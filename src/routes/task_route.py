from typing import Annotated, Union
from fastapi import APIRouter, Depends, HTTPException, Header, Request

from sqlalchemy.orm import Session
from dependencies import get_db
from schemas.task_schema import TaskCreateRequest, TaskEditRequest, TaskResponse, TaskUndoRequest
from services import task_service

task_router = APIRouter()

@task_router.get("", response_model=list[TaskResponse])
def get_all_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return task_service.get_tasks(db, skip=skip, limit=limit)

@task_router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: str, db: Session = Depends(get_db)):
    return task_service.find_task_by_id(db, task_id=task_id)

@task_router.get("/deleted/{task_id}", response_model=TaskResponse)
def get_task(task_id: str, db: Session = Depends(get_db)):
    return task_service.find_task_by_id(db, task_id=task_id, inc_deleted=True)

@task_router.post("", response_model=TaskResponse)
def create_task(user_id: Annotated[Union[str, None], Header()], task: TaskCreateRequest, db: Session = Depends(get_db)):
    return task_service.create_task(db, user_id, task)

@task_router.post("/{task_id}/edit", response_model=TaskResponse)
def edit_task(user_id: Annotated[Union[str, None], Header()], task_id: str, edit_task: TaskEditRequest, db: Session = Depends(get_db)):
    return task_service.edit_task(db, user_id, task_id, edit_task)

@task_router.post("/{task_id}/undo")
def undo_edited_task(user_id: Annotated[Union[str, None], Header()], task_id: str, undo_req: TaskUndoRequest, db: Session = Depends(get_db)):
    return task_service.undo_edited_task(db, user_id, task_id, undo_req.undo_depth)

@task_router.delete("/{task_id}")
def delete_task(user_id: Annotated[Union[str, None], Header()], task_id: str, db: Session = Depends(get_db)):
    task_service.delete_task_by_id(db, user_id, task_id)    
    return { "status" : "success"}

@task_router.post("/clear-deleted-tasks")
def clear_all_deleted_tasks(db: Session = Depends(get_db)):
    num = task_service.clear_all_deleted_task(db)
    return { "deleted_items": num}
