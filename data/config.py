from pathlib import Path

BOT_TOKEN = ''
LOGS_BASE_PATH = str(Path(__file__).parent.parent / 'logs')

admins = [121020442, 1496429325]

ip = {
    'db':    'localhost',
    'redis': 'localhost',
}

mysql_info = {
    'host':     ip['db'],
    'user':     '',
    'password': '',
    'db':       '',
    'maxsize':  5,
    'port':     3306,
}

redis = {
    'host':     ip['redis'],
    'password': ''
}
