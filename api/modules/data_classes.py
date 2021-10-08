from pydantic import BaseModel
from typing import Optional

# Pydantic data classes definition------------------------------------


# Data class for User response verification
class BaseUser(BaseModel):
    id: str
    name: str
    email: str


# Data class for new User request verification
class InUser(BaseUser):
    password: str


# Data class for User update request verification
class UpdateUser(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None


# Data class for Team response and new Team request verification
class BaseTeam(BaseModel):
    id: str
    name: str
    description: str


# Data class for Team update request verification
class UpdateTeam(BaseTeam):
    name: Optional[str] = None
    description: Optional[str] = None
