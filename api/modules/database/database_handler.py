from abc import ABC, abstractmethod
from api.modules.data_classes import *


class DBHandler(ABC):
    """
    Abstract base class for database handlers. Classes that inherit this
    class should implement the respective logic for managing interactions
    with a specific database engine.
    """

    @abstractmethod
    async def select_user(self, user_id: str):
        pass

    @abstractmethod
    async def select_users(self):
        pass

    @abstractmethod
    async def insert_user(self, new_user: InUser):
        pass

    @abstractmethod
    async def update_user(self, user_id: str, new_data: UpdateUser):
        pass

    @abstractmethod
    async def delete_user(self, user_id: str):
        pass

    @abstractmethod
    async def select_team(self, team_id: str):
        pass

    @abstractmethod
    async def select_teams(self):
        pass

    @abstractmethod
    async def insert_team(self, new_team: BaseTeam):
        pass

    @abstractmethod
    async def update_team(self, team_id: str, new_data: UpdateTeam):
        pass

    @abstractmethod
    async def delete_team(self, team_id: str):
        pass

    @abstractmethod
    async def select_user_teams(self, user_id: str):
        pass

    @abstractmethod
    async def select_team_members(self, team_id: str):
        pass

    @abstractmethod
    async def insert_team_member(self, team_id: str, user_id: str):
        pass

    @abstractmethod
    async def delete_team_member(self, team_id: str, user_id: str):
        pass

