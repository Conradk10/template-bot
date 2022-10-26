from loader import bot
from utils import get_free_sql, get_user_data, update_user_respect
from loguru import logger


async def do_payday():
    """
    Пейдей
    TODO: Во время пейдей:
    TODO: Игрокам: прибавлять опыт
    TODO:
    """
    logger.info("Payday started")

    # Настройки пейдея
    payday_data = get_free_sql(
        "SELECT setting, int_value FROM settings "
        "WHERE setting IN ('payday_exp')",
        fetchall=True
    )
    # Множитель опыта, множитель зарплаты, пособие о безработице
    payday_exp = 1
    for _ in payday_data:
        if _['setting'] == 'payday_exp':
            payday_exp = _['int_value']

    # Берем интервал для пейдея - 168 часов (1 неделя)
    pd_interval = (get_free_sql("SELECT DATE_ADD(SYSDATE(), INTERVAL -168 HOUR) AS pd_interval"))["pd_interval"]

    # Всем юзерам добавляем респекты
    get_free_sql(
        "UPDATE users SET "
        ""
        "respect = respect + %s "
        "WHERE last_action >= %s",
        (payday_exp,
         pd_interval)
    )

    # Берем всех юзеров кто был онлайн за час
    users_data = get_free_sql(
        "SELECT * FROM users WHERE last_action >= %s",
        (pd_interval,),
        fetchall=True
    )

    for user_data in users_data:
        await update_user_respect(user_data['uid'], user_data=user_data)

    logger.info("Payday OK")
    return True


async def do_checkout():
    """ Отправлять всем сообщение о банковском чеке """
    logger.info("Checkout started")

    # Настройки пейдея
    payday_data = get_free_sql(
        "SELECT setting, int_value FROM settings "
        "WHERE setting IN ('payday_exp', 'payday_salary', 'payday_nojob')",
        fetchall=True
    )
    # Множитель опыта, множитель зарплаты, пособие о безработице
    payday_exp, payday_salary, payday_nojob = 0, 0, 0
    for _ in payday_data:
        if _['setting'] == 'payday_exp':
            payday_exp = _['int_value']
        elif _['setting'] == 'payday_salary':
            payday_salary = _['int_value']
        elif _['setting'] == 'payday_nojob':
            payday_nojob = _['int_value']

    # Берем интервал для пейдея - 168 часов (1 неделя)
    pd_interval = (get_free_sql("SELECT DATE_ADD(SYSDATE(), INTERVAL -168 HOUR) AS pd_interval"))["pd_interval"]

    # Пополнение всем
    get_free_sql(
        "UPDATE users SET "
        ""
        "money = money + salary * %s, "
        "last_salary = salary * %s, "
        "salary = 0, "
        "money = money + IF(job <= 0, %s, 0) "
        ""
        "WHERE last_action >= %s",
        (payday_salary, payday_salary, payday_nojob,
         pd_interval)
    )

    # Берем всех юзеров кто был онлайн за час
    users_data = get_free_sql(
        "SELECT * FROM users WHERE last_action >= %s",
        (pd_interval,),
        fetchall=True
    )

    # Payday рассылка и пересчет
    for user_data in users_data:
        user_data = await get_user_data(user_data['uid'], user_data=user_data, fast_mode=True)

        text = '🧾 <b>Банковский чек</b>\n\n' \
               f'<b>Уровень</b>: <code>{user_data["level"]}</code>\n' \
               f'<b>Уважение</b>: <code>{user_data["curr_respect"]}</code>/' \
               f'<code>{user_data["next_respect"]}</code>\n' \
               f'<b>Зарплата</b>: $<code>{user_data["last_salary"]}</code>\n'
        if user_data['job'] <= 0:
            text += f'<b>Пособие по безработице</b>: $<code>{payday_nojob}</code>\n'
        await bot.send_message(user_data['uid'], text=text)

    logger.info("Checkout OK")

    return True
