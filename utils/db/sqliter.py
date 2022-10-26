import logging
import pymysql
from utils.misc.logging import logger
from data.config import mysql_info as db

connection = pymysql.connect(db['host'], db['user'], db['password'], db['db'], cursorclass=pymysql.cursors.DictCursor,
                             autocommit=True, init_command=logger.info("БД успешно подключена!"))


def logger(statement):
    logging.basicConfig(
        level=logging.INFO,
        filename="logs.log",
        format=f"[Executing] [%(asctime)s] | [%(filename)s LINE:%(lineno)d] | {statement}",
        datefmt="%d-%b-%y %H:%M:%S"
    )
    logging.info(statement)


def handle_silently(function):
    def wrapped(*args, **kwargs):
        result = None
        try:
            result = function(*args, **kwargs)
        except Exception as e:
            logger("{}({}, {}) failed with exception {}".format(
                function.__name__, repr(args[1]), repr(kwargs), repr(e)))
        return result

    return wrapped


# Форматирование запроса с аргументами
def update_format_with_args(sql, parameters: dict):
    values = ", ".join([
        f"{item} = ?" for item in parameters
    ])
    sql = sql.replace("XXX", values)
    return sql, tuple(parameters.values())


# Форматирование запроса без аргументов
def get_format_args(sql, parameters: dict):
    sql += " AND ".join([
        f"{item} = ?" for item in parameters
    ])
    return sql, tuple(parameters.values())


# Получение пользователя
def get_free_sql(query: str, args=None, fetchall=False):
    connection.ping()
    with connection.cursor() as cursor:
        cursor.execute(query, args)
        if fetchall: response = cursor.fetchall()
        else: response = cursor.fetchone()
    return response
