
# Module for saving connection configuration of possible database handlers
# Import appropriately inside each database_handler implementation module

CONFIG_SQLITE = {
    "production": {
        "db_file": "MainDB.db"
    },
    "test": {
        "db_file": "tests/database/TempDB.db"
    }
}