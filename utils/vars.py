from utils.db.sqliter import get_free_sql


levels_data = get_free_sql("SELECT * FROM levels", fetchall=True)


def update_levels_data() -> levels_data:
    global levels_data
    levels_data = get_free_sql("SELECT * FROM levels", fetchall=True)
    return levels_data
