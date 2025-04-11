# app/utils/utils.py

# Стандартные модули Python
# import aiohttp

# # Сторонние модули
# from aiogram.types import Message

# # Собственные модули
# from app.utils.token_utils import prepare_user_info, generate_token
# from app.config import ADD_CHAT_ID_URL, BASE_URL, WEB_APP_URL

# from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, WebAppInfo


# async def check_user_access(message: Message):
#     """
#     Отправляет запрос к API для проверки доступа.
#     """
#     try:
#         # Отправка запроса к API для проверки наличия пользователя в бд
#         user_info = prepare_user_info(message)
#         token = generate_token(user_info)
#         async with aiohttp.ClientSession() as session:
#             async with session.post(ADD_CHAT_ID_URL, json={"token": token}) as response:
#                 if response.status == 403:
#                     raise Exception(await response.json())
#                 return await response.json()
#     except Exception as e:
#         # Если возникла ошибка, отправляем сообщение об ошибке пользователю
#         error_detail = getattr(e, 'args', ["Ошибка без деталей"])[0]
#         if isinstance(error_detail, dict) and "detail" in error_detail:
#             error_message = error_detail["detail"]
#         else:
#             error_message = str(error_detail)

#         await message.answer(f"Ошибка: {error_message}")
#         return

# async def air_balon_and_swings(message: Message):
#     # Извлекаем username из объекта message
#     tg_username = message.from_user.username
#     chat_id = message.chat.id

#     # Создаем ссылку с параметром username
#     swing_url = f"{WEB_APP_URL}bot_swing?username={tg_username}"
#     air_ballon_url = f"{WEB_APP_URL}bot_air_balon?username={tg_username}"
#     flight_url = f"{WEB_APP_URL}flight?user_id={chat_id}"

#     # Создаем клавиатуру с кнопками в одну линию
#     keyboard = ReplyKeyboardMarkup(
#         keyboard=[
#             [
#                 KeyboardButton(
#                     text="Качели",
#                     web_app=WebAppInfo(url=swing_url)
#                 ),
#                 KeyboardButton(
#                     text="Воздушный шар",
#                     web_app=WebAppInfo(url=air_ballon_url)
#                 ),
#                 KeyboardButton(
#                     text="Доходы",
#                     web_app=WebAppInfo(url=flight_url)
#                 )
#             ]
#         ],
#         resize_keyboard=True
#     )

#     # Отправляем сообщение с кнопками в клавиатуре
#     await message.answer(
#         text="Внесите доход",
#         reply_markup=keyboard
#     )



# Стандартные модули Python
import aiohttp
# Сторонние модули
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import Bot, Dispatcher, types
# Собственные модули
from app.utils.token_utils import prepare_user_info, generate_token
from app.config import ADD_CHAT_ID_URL, BASE_URL, WEB_APP_URL, TOKEN

bot = Bot(token = TOKEN)
dp = Dispatcher()
# Список пользователей и их доступных кнопок
ALLOWED_USERS = {
    "heytward": "Запись рейсов",
    "axm9t": "Запись рейсов",
    "Vladislav_Arkhipov": "Внести доход",
    "tokov17": "Качели",
    "Q5fantan": "Запись рейсов",
    "Pavel_Er": "Внести доход"
}

# Словарь для URL кнопок
BUTTON_URLS = {
    "Запись рейсов": lambda user_id: f"http://127.0.0.1:8000/flight?user_id==702856294",
    "Внести доход": lambda username: f"{WEB_APP_URL}bot_air_balon?username={username}",
    "Качели": lambda username: f"{WEB_APP_URL}bot_swing?username={username}"
}

async def check_user_access(message: Message):
    """
    Проверяет доступ пользователя.
    """
    try:
        user_info = prepare_user_info(message)
        token = generate_token(user_info)

        async with aiohttp.ClientSession() as session:
            async with session.post(ADD_CHAT_ID_URL, json={"token": token}) as response:
                if response.status == 403:
                    raise Exception(await response.json())
                return await response.json()
    except Exception as e:
        error_detail = getattr(e, 'args', ["Ошибка без деталей"])[0]
        error_message = error_detail.get("detail", str(error_detail)) if isinstance(error_detail, dict) else str(error_detail)
        await message.answer(f"Ошибка: {error_message}")
        return



async def create_reply_markupButton(message: Message) -> InlineKeyboardMarkup | None:
    tg_username = message.from_user.username

    if tg_username not in ALLOWED_USERS:
        return None

    button_text = ALLOWED_USERS[tg_username]
    if button_text not in BUTTON_URLS:
        return None

    url = BUTTON_URLS[button_text](tg_username)
    print(f"Generated URL: {url}")  # Для отладки

    if button_text == "Внести доход":
        first_button = InlineKeyboardButton(text="Внести доход", web_app=WebAppInfo(url=url))
        second_button = InlineKeyboardButton(text="Внести расход", web_app=WebAppInfo(url=url))
        markup = InlineKeyboardMarkup(inline_keyboard=[[first_button], [second_button]])
    else:
        button = InlineKeyboardButton(text=button_text, web_app=WebAppInfo(url=url))
        markup = InlineKeyboardMarkup(inline_keyboard=[[button]])

    return markup


# Обработчик для ReplyKeyboardMarkup
async def get_income_keyboard(message: Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Внести доход")]],
        resize_keyboard=True
    )
    await message.answer(
        text="Внесите доход:",
        reply_markup=keyboard
    )
