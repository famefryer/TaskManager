from sqlalchemy import Enum
from enum import Enum
from db.database import Base

class TaskStatus(Enum):
    DRAFT = 1
    OPEN = 2
    IN_PROGRESS = 3
    DONE = 4
    CANCELLED = 5
    DELETED = 6
    
class TaskPermissionLevel(Enum):
    VIEW = 1
    EDIT = 2
    DELETE = 3
    
class TaskPermissionType(Enum):
    USER = 1
    TEAM = 2
