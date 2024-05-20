from fastapi import APIRouter
from .user_route import user_router
from .team_route import team_router
from .task_route import task_router

router = APIRouter()

router.include_router(user_router, prefix="/users")
router.include_router(team_router, prefix="/teams")
router.include_router(task_router, prefix="/tasks")
