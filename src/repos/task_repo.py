from typing import overload
from sqlalchemy import func
from sqlalchemy.orm import Session

from models.task_model import (
    Task,
    TaskHistory,
    TaskPermission,
    TaskPermissionLevel,
    TaskPermissionType,
    TaskStatus,
)
from schemas.task_schema import TaskCreateRequest, TaskEditRequest


def get_all_tasks(db: Session, skip: int, limit: int, inc_deleted: bool) -> list[Task]:
    query = db.query(Task)
    if not inc_deleted:
        query = query.where(Task.deleted_at == None)
    return query.offset(skip).limit(limit).all()

def find_task_by_id(db: Session, id: int, inc_deleted: bool) -> Task:
    query = db.query(Task)
    if not inc_deleted:
        query = query.where(Task.deleted_at == None)
    return query.where(Task.id == id).first()

def create_task(db: Session, user_id, use_perm: bool, task: TaskCreateRequest) -> Task:
    db_task = Task(
        topic=task.topic,
        description=task.description,
        created_by=user_id,
        assignee=task.assignee_id,
        use_permission=use_perm,
    )
    db.add(db_task)
    db.commit()

    return db_task


def find_task_permission(
    db: Session, task_id: str, perm_ent_id: str, task_perm_type: TaskPermissionType
) -> TaskPermission:
    return (
        db.query(TaskPermission)
        .where(
            TaskPermission.task_id == task_id,
            TaskPermission.permission_entity_id == perm_ent_id,
            TaskPermission.permission_type == task_perm_type,
        )
        .first()
    )


def add_task_permission(
    db: Session,
    task_id: str,
    perm_ent_id: str,
    perm_type: TaskPermissionType,
    perm_level: TaskPermissionLevel,
) -> TaskPermission:
    db_task_perm = TaskPermission(
        task_id=task_id,
        permission_entity_id=perm_ent_id,
        permission_type=perm_type,
        permission_level=perm_level,
    )
    db.add(db_task_perm)
    db.commit()

    return db_task_perm

def update_task(db: Session, db_task: Task, edited_task: TaskEditRequest):
    db_task.version = db_task.version + 1
    if edited_task.topic is not None:
        db_task.topic = edited_task.topic
    if edited_task.description is not None:
        db_task.description = edited_task.description
    if edited_task.status is not None:
        db_task.status = edited_task.status
    if edited_task.assignee_id is not None:
        db_task.assignee = edited_task.assignee_id

    db.commit()

def update_task_by_task_history(db: Session, db_task: Task, task_history: TaskHistory) -> Task:
    db_task.version = task_history.version
    db_task.topic = task_history.topic
    db_task.description = task_history.description
    db_task.status = task_history.status
    db_task.assignee = task_history.assignee
    db_task.use_permission = task_history.use_permission

    db.commit()
    
    return db_task


def delete_task(db: Session, task: Task):
    task.deleted_at = func.now()
    db.commit()

def delete_all_soft_deleted_tasks(db: Session) -> int:
    res = db.query(Task).filter(Task.deleted_at != None).delete()
    res = db.query(TaskHistory).filter(TaskHistory.deleted_at != None).delete()
    db.commit()
    return res


def find_task_history(db: Session, task_id: str, version: int):
    return (
        db.query(TaskHistory)
        .where(TaskHistory.task_id == task_id, TaskHistory.version == version)
        .first()
    )

def create_task_history(db: Session, user_id: str, task: Task) -> TaskHistory:
    task_history = TaskHistory(
        task_id=task.id,
        version=task.version,
        topic=task.topic,
        description=task.description,
        status=task.status,
        assignee=task.assignee,
        use_permission=task.use_permission,
        edited_by=user_id,
    )
    db.add(task_history)
    db.commit()

    return task_history

def delete_newer_task_history(db: Session, task_id: str, cur_version: int):
    res = (
        db.query(TaskHistory)
        .filter(TaskHistory.task_id == task_id, TaskHistory.version >= cur_version)
        .delete()
    )
    db.commit()
    return res

def delete_task_history_by_task_id(db: Session, task_id: str):
    task_histories = db.query(TaskHistory).filter(TaskHistory.task_id == task_id).all()
    for task_h in task_histories:
        task_h.deleted_at = func.now()
    db.commit()
