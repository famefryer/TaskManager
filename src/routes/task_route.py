from typing import Annotated, Union
from fastapi import APIRouter, Depends, HTTPException, Header, Request

from sqlalchemy.orm import Session
from dependencies import get_db
from schemas.task_schema import (
    TaskCreateRequest,
    TaskEditRequest,
    TaskHistoryResponse,
    TaskResponse,
    TaskRestoreRequest,
    TaskUndoRequest,
)
from services import task_service

task_router = APIRouter()


@task_router.get("", response_model=list[TaskResponse])
def get_all_tasks(
    created_by: str = None,
    assignee: str = None,
    skip: int = 0,
    limit: int = 100,
    include_soft_deleted: bool = False,
    db: Session = Depends(get_db),
):
    return task_service.get_tasks(
        db, skip=skip, limit=limit, inc_deleted=include_soft_deleted, created_by=created_by, assignee=assignee
    )


@task_router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: str, db: Session = Depends(get_db)):
    return task_service.find_task_by_id(db, task_id=task_id)


@task_router.get("/deleted/{task_id}", response_model=TaskResponse)
def get_task(task_id: str, db: Session = Depends(get_db)):
    return task_service.find_task_by_id(db, task_id=task_id, inc_deleted=True)


@task_router.post("", response_model=TaskResponse)
def create_task(
    user_id: Annotated[Union[str, None], Header()],
    task: TaskCreateRequest,
    db: Session = Depends(get_db),
):
    return task_service.create_task(db, user_id=user_id, task=task)


@task_router.post("/{task_id}/edit", response_model=TaskResponse)
def edit_task(
    user_id: Annotated[Union[str, None], Header()],
    task_id: str,
    edit_task: TaskEditRequest,
    db: Session = Depends(get_db),
):
    return task_service.edit_task(
        db, user_id=user_id, task_id=task_id, edited_task=edit_task
    )


@task_router.post("/{task_id}/undo", response_model=TaskResponse)
def undo_edited_task(
    task_id: str, undo_req: TaskUndoRequest, db: Session = Depends(get_db)
):
    return task_service.undo_edited_task(
        db, task_id=task_id, undo_depth=undo_req.undo_depth
    )


@task_router.delete("/{task_id}")
def delete_task(task_id: str, db: Session = Depends(get_db)):
    task_service.delete_task_by_id(db, task_id)
    return {"status": "success"}


@task_router.post("/clear-deleted-tasks")
def clear_all_deleted_tasks(db: Session = Depends(get_db)):
    num = task_service.clear_all_deleted_task(db)
    return {"deleted_items": num}


@task_router.get("/{task_id}/history", response_model=list[TaskHistoryResponse])
def get_task_history(task_id: str, db: Session = Depends(get_db)):
    return task_service.get_all_task_history(db, task_id=task_id)


@task_router.post("/restore")
def restore_deleted_tasks(req: TaskRestoreRequest, db: Session = Depends(get_db)):
    num = task_service.restore_deleted_tasks(db, task_ids=req.task_ids)
    return {"restore_items": num}
