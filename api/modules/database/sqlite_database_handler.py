import aiosqlite

from api.modules.data_classes import UpdateTeam, BaseTeam, UpdateUser, InUser
from database_handler import DBHandler
from config import CONFIG_SQLITE
from utils import encrypt_string, generate_sql_update_set_formatted_string

# Establish necessary connection configuration for SQLite db
connection_config = CONFIG_SQLITE.production.db_file


class SQLiteDBHandler(DBHandler):
    """
    DB handler class for managing operations on a SQLite db.
    Singleton class, just allows for one instance at any given time
    """

    _instance = None  # Class instance of same class (singleton pattern)

    # Overriding of __new__ method for implementing singleton pattern
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__()

        return cls._instance

    async def select_user(self, user_id: str):
        """
        Select a single row from users table in DB

        :param user_id: Id of user of interest
        :return: Single list corresponding to the user record, uses format ["id", "name", "email"]
        """
        resulting_row = []
        async with aiosqlite.connect(connection_config) as db:
            cursor = await db.execute('SELECT id, name, email FROM users WHERE id=:id', {"id": user_id})
            resulting_row = await cursor.fetchone()

            await cursor.close()

        return resulting_row

    async def select_users(self):
        """
        Select all rows from users table in DB

        :return: A list corresponding to all user records, uses format [["id", "name", "email"],...]
        """
        resulting_rows = []
        async with aiosqlite.connect(connection_config) as db:
            cursor = await db.execute('SELECT id, name, email FROM users')
            resulting_rows = await cursor.fetchall()

            await cursor.close()

        return resulting_rows

    async def insert_user(self, new_user: InUser):
        """
        Insert a new record to the users table in DB

        :param new_user: Pydantic model with the new user data
        :return: Single list corresponding to inserted user record, uses format ["id", "name", "email"]
        """
        inserted_row = []
        new_user.password = encrypt_string(new_user.password)

        async with aiosqlite.connect(connection_config) as db:
            await db.execute("INSERT INTO users values (:id, :name, :email, :password)", new_user.dict())
            await db.commit()

        inserted_row = await self.select_user(user_id=new_user.id)
        return inserted_row

    async def update_user(self, user_id: str, new_data: UpdateUser):
        """
        Update record of an existing user in the DB

        :param user_id: Id of user of interest
        :param new_data: Pydantic model with the new user data
        :return: Single list corresponding to updated user record, uses format ["id", "name", "email"]
        """
        updated_row = []
        if new_data.password:
            new_data.password = encrypt_string(new_data.password)

        updated_values_dict = new_data.dict(exclude_unset=True)

        set_query = generate_sql_update_set_formatted_string(list(updated_values_dict.keys()))
        updated_values_dict["id"] = user_id

        async with aiosqlite.connect(connection_config) as db:
            await db.execute(f"UPDATE users SET {set_query} WHERE id = :id", updated_values_dict)
            await db.commit()

        updated_row = await self.select_user(user_id=user_id)
        return updated_row

    async def delete_user(self, user_id: str):
        """
        Delete a record from the users table in DB.
        Also deletes all related records of the user in team_members table

        :param user_id: Id of user of interest
        :return: Single list corresponding to deleted user record, uses format ["id", "name", "email"]
        """
        deleted_row = await self.select_user(user_id=user_id)

        async with aiosqlite.connect(connection_config) as db:
            await db.execute("DELETE FROM team_members WHERE id_user = :id", {"id": user_id})
            await db.execute("DELETE FROM users WHERE id = :id", {"id": user_id})
            await db.commit()

        return deleted_row

    async def select_team(self, team_id: str):
        """
        Select a single row from teams table in DB

        :param team_id: Id of team of interest
        :return: Single list corresponding to the team record, uses format ["id", "name", "description"]
        """
        resulting_row = []
        async with aiosqlite.connect(connection_config) as db:
            cursor = await db.execute('SELECT * FROM teams WHERE id=:id', {"id": team_id})
            resulting_row = await cursor.fetchone()

            await cursor.close()

        return resulting_row

    async def select_teams(self):
        """
        Select all rows from teams table in DB

        :return: A list corresponding to all team records, uses format [["id", "name", "description"],...]
        """
        resulting_rows = []
        async with aiosqlite.connect(connection_config) as db:
            cursor = await db.execute('SELECT * FROM teams')
            resulting_rows = await cursor.fetchall()

            await cursor.close()

        return resulting_rows

    async def insert_team(self, new_team: BaseTeam):
        """
        Insert a new record to the teams table in DB

        :param new_team: Pydantic model with the new team data
        :return: Single list corresponding to inserted team record, uses format ["id", "name", "description"]
        """
        inserted_row = []

        async with aiosqlite.connect(connection_config) as db:
            await db.execute("INSERT INTO teams values (:id, :name, :description)", new_team.dict())
            await db.commit()

        inserted_row = await self.select_team(team_id=new_team.id)
        return inserted_row

    async def update_team(self, team_id: str, new_data: UpdateTeam):
        """
        Update record of an existing team in the DB

        :param team_id: Id of team of interest
        :param new_data: Pydantic model with the new team data
        :return: Single list corresponding to updated team record, uses format ["id", "name", "description"]
        """
        updated_row = []

        updated_values_dict = new_data.dict(exclude_unset=True)

        set_query = generate_sql_update_set_formatted_string(list(updated_values_dict.keys()))
        updated_values_dict["id"] = team_id

        async with aiosqlite.connect(connection_config) as db:
            await db.execute(f"UPDATE teams SET {set_query} WHERE id = :id", updated_values_dict)
            await db.commit()

        updated_row = await self.select_team(team_id=team_id)
        return updated_row

    async def delete_team(self, team_id: str):
        """
        Delete a record from the teams table in DB.
        Also deletes all related records of the team in team_members table

        :param team_id: Id of team of interest
        :return: Single list corresponding to deleted team record, uses format ["id", "name", "description"]
        """
        deleted_row = await self.select_team(team_id=team_id)

        async with aiosqlite.connect(connection_config) as db:
            await db.execute("DELETE FROM team_members WHERE id_team = :id", {"id": team_id})
            await db.execute("DELETE FROM teams WHERE id = :id", {"id": team_id})
            await db.commit()

        return deleted_row

    async def select_user_teams(self, user_id: str):
        """
        Select all rows from teams where a user is a member

        :param user_id: Id of user of interest
        :return: A list of all team records associated with a user, uses format [["id", "name", "description"],...]
        """
        resulting_rows = []
        async with aiosqlite.connect(connection_config) as db:
            cursor = await db.execute(('SELECT teams.id, teams.name, teams.description '
                                       'FROM teams INNER JOIN team_members on teams.id = team_members.id_team'
                                       'WHERE team_members.id_user = :id_user'), {"id_user": user_id})
            resulting_rows = await cursor.fetchall()

            await cursor.close()

        return resulting_rows

    async def select_team_members(self, team_id: str):
        """
        Select all rows from users that are members of a team

        :param team_id: Id of team of interest
        :return: A list of all user records associated with a team, uses format [["id", "name", "email"],...]
        """
        resulting_rows = []
        async with aiosqlite.connect(connection_config) as db:
            cursor = await db.execute(('SELECT users.id, users.name, users.email '
                                       'FROM users INNER JOIN team_members on users.id = team_members.id_user'
                                       'WHERE team_members.id_team = :id_team'), {"id_team": team_id})
            resulting_rows = await cursor.fetchall()

            await cursor.close()

        return resulting_rows

    async def insert_team_member(self, team_id: str, user_id: str):
        """
        Insert a new record to the team_members table in DB

        :param team_id: Id of team of interest
        :param user_id: Id of user of interest
        :return: Single list corresponding to the inserted team_member record, uses format ["id_team", "id_user"]
        """
        inserted_row = []

        async with aiosqlite.connect(connection_config) as db:
            await db.execute("INSERT INTO team_members values (:id_team, :id_user)", {"id_team": team_id, "id_user": user_id})
            await db.commit()

            cursor = await db.execute(('SELECT id_team, id_user FROM team_members'
                                       'WHERE id_team = :id_team AND id_user = :id_user'),
                                      {"id_team": team_id, "id_user": user_id})
            inserted_row = await cursor.fetchone()
            await cursor.close()

        return inserted_row

    async def delete_team_member(self, team_id: str, user_id: str):
        """
        Delete a record from the team_members table in DB

        :param team_id: Id of team of interest
        :param user_id: Id of user of interest
        :return: Single list corresponding to deleted team_member record, uses format ["id_team", "id_user"]
        """
        deleted_row = []

        async with aiosqlite.connect(connection_config) as db:
            cursor = await db.execute(('SELECT id_team, id_user FROM team_members'
                                       'WHERE id_team = :id_team AND id_user = :id_user'),
                                      {"id_team": team_id, "id_user": user_id})
            deleted_row = await cursor.fetchone()
            await cursor.close()

            await db.execute(("DELETE FROM team_members "
                              "WHERE id_team = :id_team AND id_user = :id_user"),
                             {"id_team": team_id, "id_user": user_id})
            await db.commit()

        return deleted_row
