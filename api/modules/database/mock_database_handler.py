from api.modules.data_classes import UpdateTeam, BaseTeam, UpdateUser, InUser
from .database_handler import DBHandler, DBHandlerException


class MockDBHandler(DBHandler):
    """
    Mock database handler for testing normal behavior of FastAPI endpoints.
    All methods just return default hard-coded values according to the expected behavior
    of well implemented logic
    """

    async def select_user(self, user_id: str):
        return user_id, "my_name", "my_email"

    async def select_users(self):
        return [("my_id_1", "my_name_1", "my_email_1"), ("my_id_2", "my_name_2", "my_email_2")]

    async def insert_user(self, new_user: InUser):
        return new_user.id, new_user.name, new_user.email

    async def update_user(self, user_id: str, new_data: UpdateUser):
        return user_id, new_data.name, new_data.email

    async def delete_user(self, user_id: str):
        return user_id, "my_name", "my_email"

    async def select_team(self, team_id: str):
        return team_id, "my_name", "my_description"

    async def select_teams(self):
        return [("my_id_1", "my_name_1", "my_description_1"), ("my_id_2", "my_name_2", "my_description_2")]

    async def insert_team(self, new_team: BaseTeam):
        return new_team.id, new_team.name, new_team.description

    async def update_team(self, team_id: str, new_data: UpdateTeam):
        return team_id, new_data.name, new_data.description

    async def delete_team(self, team_id: str):
        return team_id, "my_name", "my_description"

    async def select_user_teams(self, user_id: str):
        return [("my_id_1", "my_name_1", "my_description_1"), ("my_id_2", "my_name_2", "my_description_2")]

    async def select_team_members(self, team_id: str):
        return [("my_id_1", "my_name_1", "my_email_1"), ("my_id_2", "my_name_2", "my_email_2")]

    async def insert_team_member(self, team_id: str, user_id: str):
        return team_id, user_id

    async def delete_team_member(self, team_id: str, user_id: str):
        return team_id, user_id


class MockErrorDBHandler(MockDBHandler):
    """
    Mock database handler for testing unwanted interactions in the DB. Raises the appropriate
    exceptions to emulate integrity errors while trying to run pertinent actions
    """

    async def insert_user(self, new_user: InUser):
        raise DBHandlerException()

    async def update_user(self, user_id: str, new_data: UpdateUser):
        raise DBHandlerException()

    async def insert_team(self, new_team: BaseTeam):
        raise DBHandlerException()

    async def update_team(self, team_id: str, new_data: UpdateTeam):
        raise DBHandlerException()

    async def insert_team_member(self, team_id: str, user_id: str):
        raise DBHandlerException()

