from asyncio.windows_events import NULL
import redis
import logging
import datetime

from config import *
from functions import BD

from vkbottle.bot import Bot, Message
from vkbottle import Keyboard, Text

bot = Bot(token=TOKEN)

date_str = datetime.datetime.now().strftime('%m-%d-%y_%H_%M')
logger = logging.basicConfig(filename=f"logs\\{date_str}_log.log", level=logging.INFO)

cash = {}

# for admin in ADMINS:
#     cash[admin] = ""

bd = BD()

user_keyboard = Keyboard(one_time=False).add(Text("-> 📌 Личный кабинет", {"profile": "local"})
                                 ).row().add(Text("-> ✏ О занятиях", {"lessons": "local"})
                                 ).row().add(Text("-> 💳 Оплатить", {"payment": "local"})
                                 ).row().add(Text("-> ❓ Задать вопрос", {"question": "local"})
                                 ).get_json()

admin_keyboard = Keyboard(one_time=False).add(Text("-> Создать ученика", {"new_user": "local"})
                                  ).row().add(Text("-> Изменить ученика", {"edit_user": "local"})
                                  ).row().add(Text("-> Ученики/Users", {"get_users": "local"})
                                  ).row().add(Text("-> Ученик/User", {"get_user": "local"})
                                  ).row().add(Text("-> Информация о оплате", {"get_payment": "local"})
                                  ).row().add(Text("-> Изменить информацию о оплате", {"edit_payment": "local"})
                                  ).get_json()

@bot.on.private_message(payload={"profile": "local"})
async def profile(msg: Message):
    #print("Profile " + msg.from_id)
    await msg.answer(bd.get_profile(msg.from_id), keyboard=user_keyboard)

@bot.on.private_message(payload={"lessons": "local"})
async def lessons(msg: Message):
    #print("Lessons " + msg.from_id)
    await msg.answer(bd.get_lesson(msg.from_id), keyboard=user_keyboard)


@bot.on.private_message(payload={"payment": "local"})
async def lessons(msg: Message):
    await msg.answer(bd.get_payment(), keyboard=user_keyboard)


@bot.on.private_message(payload={"question": "local"})
async def lessons(msg: Message):
    cash[msg.from_id] = "question"
    await msg.answer("Напишите свой вопрос:", keyboard=user_keyboard)


@bot.on.private_message(payload={"get_payment": "local"})
async def lessons(msg: Message):
    await msg.answer(bd.get_payment(), keyboard=admin_keyboard)


@bot.on.private_message(payload={"edit_payment": "local"})
async def lessons(msg: Message):
    cash[msg.from_id] = "edit_payment"
    await msg.answer("Введите новую информацию о полате:", keyboard=admin_keyboard)


@bot.on.private_message(payload={"new_user": "local"})
async def lessons(msg: Message):
    cash[msg.from_id] = "new_user"
    await msg.answer("Введите VKid нового пользователя:", keyboard=admin_keyboard)


@bot.on.private_message(payload={"get_user": "local"})
async def lessons(msg: Message):
    cash[msg.from_id] = "get_user"
    await msg.answer("Введите VKid пользователя:", keyboard=admin_keyboard)


@bot.on.private_message(payload={"get_users": "local"})
async def lessons(msg: Message):
    await msg.answer(bd.get_users(), keyboard=admin_keyboard)


@bot.on.private_message(payload={"edit_user": "local"})
async def lessons(msg: Message):
    cash[msg.from_id] = "edit_user"
    await msg.answer("""Введите новую информацию формата:
VKid ученика
Имя ученика
Возраст ученика
Курс ученика
Уровень обучения ученика
Пол ученика
Имя родителя
Номер родителя
Домашние задание""", keyboard=admin_keyboard)


@bot.on.private_message()
async def msg(msg: Message):
    if msg.from_id in ADMINS:
        if (msg.from_id not in cash) or cash[msg.from_id] == "":
            await msg.answer("Пожалуйста, используйте меню", keyboard=admin_keyboard)
        elif cash[msg.from_id] == "new_user":
            cash[msg.from_id] = ""
            await msg.answer(bd.new_user(msg.text), keyboard=admin_keyboard)
            return
        elif cash[msg.from_id] == "edit_user":
            cash[msg.from_id] = ""
            await msg.answer(bd.edit_user(msg.text), keyboard=admin_keyboard)
            return
        elif cash[msg.from_id] == "get_user":
            cash[msg.from_id] = ""
            await msg.answer(bd.get_user(msg.text), keyboard=admin_keyboard)
            return
        elif cash[msg.from_id] == "edit_payment":
            cash[msg.from_id] = ""
            await msg.answer(bd.edit_payment(msg.text), keyboard=admin_keyboard)
            return
    else:
        if (msg.from_id not in cash) or cash[msg.from_id] == "":
            await msg.answer("Пожалуйста, используйте меню", keyboard=user_keyboard)
        elif cash[msg.from_id] == "question":
            cash[msg.from_id] = ""
            await msg.answer("Вопрос задан, ждите ответа от администратора!", keyboard=user_keyboard)
            for id in ADMINS:
                await bot.api.messages.send(id, 0, message=f"@id{msg.from_id} вопрос:\n{msg.text}")


bot.run_forever()