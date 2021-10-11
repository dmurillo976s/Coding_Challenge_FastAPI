from pydantic import BaseModel, Field
from typing import Optional, Tuple

# Pydantic data classes definition------------------------------------


# Data class for User response verification
class BaseUser(BaseModel):
    id: str = Field(..., description="Unique value for identifying a user")
    name: str = Field(..., description="Common user name")
    email: str = Field(..., description="Email of the user")

    class Config:
        schema_extra = {
            "description": "Data model used for responses that carry user information",
            "example": {
                "id": "myUserID01",
                "name": "John Doe",
                "email": "jd@gmail.com"
            }
        }


def init_BaseUser(values: Tuple[str, str, str]):
    return BaseUser(id=values[0], name=values[1], email=values[2])


# Data class for new User request verification
class InUser(BaseUser):
    password: str = Field(..., description="Password string of the user")

    schema_extra = {
        "description": "Data model used for input of new user data",
        "example": {
            "id": "myUserID01",
            "name": "John Doe",
            "email": "jd@gmail.com",
            "password": "123abc"
        }
    }


# Data class for User update request verification
class UpdateUser(BaseModel):
    name: Optional[str] = Field(None, description="Optional updated name value")
    email: Optional[str] = Field(None, description="Optional updated email value")
    password: Optional[str] = Field(None, description="Optional updated password value")

    schema_extra = {
        "description": "Data model used for input of updated user data",
        "example": {
            "name": "John Doe",
            "email": "jd@gmail.com",
            "password": "123abc"
        }
    }


# Data class for Team response and new Team request verification
class BaseTeam(BaseModel):
    id: str = Field(..., description="Unique value for identifying a team")
    name: str = Field(..., description="Unique name of the team")
    description: str = Field(..., description="Simple description of the team")

    class Config:
        schema_extra = {
            "description": "Data model used for responses that carry team information",
            "example": {
                "id": "myTeamID01",
                "name": "Legends",
                "description": "Very efficient team"
            }
        }


def init_BaseTeam(values: Tuple[str, str, str]):
    return BaseTeam(id=values[0], name=values[1], description=values[2])


# Data class for Team update request verification
class UpdateTeam(BaseModel):
    name: Optional[str] = Field(None, description="Optional updated name value")
    description: Optional[str] = Field(None, description="Optional updated description value")

    class Config:
        schema_extra = {
            "description": "Data model used for input of updated team information",
            "example": {
                "name": "Legends",
                "description": "Very efficient team"
            }
        }
