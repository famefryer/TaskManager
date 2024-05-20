from sqlalchemy.orm import Session

from models.task_model import Task, TaskHistory, TaskPermissionLevel, TaskPermissionType
from schemas.task_schema import TaskCreateRequest, TaskEditRequest
from repos import task_repo, user_repo, team_repo


def get_tasks(
    db: Session, skip: int = 0, limit: int = 100, inc_deleted: bool = False
) -> list[Task]:
    return task_repo.get_all_tasks(db, skip, limit, inc_deleted)


def find_task_by_id(db: Session, task_id: str, inc_deleted: bool = False) -> Task:
    return task_repo.find_task_by_id(db, task_id, inc_deleted)


def create_task(db: Session, user_id: str, task: TaskCreateRequest) -> Task:
    use_perm = True if task.permissions is not None else False
    db_task = task_repo.create_task(db, user_id=user_id, use_perm=use_perm, task=task)

    if use_perm:
        # Add permission for task creator
        db_created_user = user_repo.find_user_by_id(db, user_id)
        task_repo.add_task_permission(
            db,
            task_id=db_task.id,
            perm_ent_id=db_created_user.permission_entity_id,
            perm_type=TaskPermissionType.USER,
            perm_level=TaskPermissionLevel.DELETE,
        )

        for user_perm in task.permissions.user_permissions:
            # Skip creator
            if user_id == user_perm.entity_id:
                continue

            db_user = user_repo.find_user_by_id(db, user_perm.entity_id)
            if db_user is None:
                raise ValueError("User does not exists")

            task_repo.add_task_permission(
                db,
                task_id=db_task.id,
                perm_ent_id=db_user.permission_entity_id,
                perm_type=TaskPermissionType.USER,
                perm_level=user_perm.permission_level,
            )

        for team_perm in task.permissions.team_permissions:
            db_team = team_repo.find_team_by_id(db, user_perm.entity_id)
            if db_team is None:
                raise ValueError("Team does not exists")

            task_repo.add_task_permission(
                db,
                task_id=db_task.id,
                perm_ent_id=db_team.permission_entity_id,
                perm_type=TaskPermissionType.TEAM,
                perm_level=team_perm.permission_level,
            )

    return db_task


def edit_task(
    db: Session, user_id: str, task_id: str, edited_task: TaskEditRequest
) -> Task:
    db_task = task_repo.find_task_by_id(db, task_id, False)
    if db_task is None:
        raise ValueError("Error task does not exist")

    task_repo.create_task_history(db, user_id, db_task)
    task_repo.update_task(db, db_task, edited_task)

    return db_task


def delete_task_by_id(db: Session, task_id: str):
    db_task = task_repo.find_task_by_id(db, task_id, False)
    if db_task is None:
        raise ValueError("Error task does not exist")

    task_repo.delete_task_history_by_task_id(db, task_id)
    task_repo.delete_task(db, db_task)


def undo_edited_task(db: Session, task_id: str, undo_depth: int):
    db_task = task_repo.find_task_by_id(db, task_id, False)
    if db_task is None:
        raise ValueError("Error task does not exist")

    undo_version = db_task.version - undo_depth
    if undo_version <= 0 or undo_version >= db_task.version:
        raise ValueError("Error invalid request.undo_depth")

    task_history = task_repo.find_task_history(db, task_id, undo_version)
    db_task = task_repo.update_task_by_task_history(
        db, db_task=db_task, task_history=task_history
    )
    task_repo.delete_newer_task_history(db, task_id, undo_version)

    return db_task


def clear_all_deleted_task(db: Session) -> int:
    res = task_repo.delete_all_soft_deleted_tasks(db)
    return res


def get_all_task_history(db: Session, task_id: str) -> list[TaskHistory]:
    return task_repo.get_all_task_history_by_task_id(db, task_id=task_id)


def restore_deleted_tasks(db: Session, task_ids: list[str]) -> int:
    tasks = task_repo.find_task_by_ids(db, ids=task_ids, inc_deleted=True)
    for task in tasks:
        task_repo.restore_task(db, task=task)
        task_histories = task_repo.get_all_task_history_by_task_id(db, task_id=task.id)
        for task_h in task_histories:
            task_repo.restore_task_history(db, task_h=task_h)

    return len(tasks)
