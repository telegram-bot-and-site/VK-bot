import redis

from config import *
from functions import BD
from vkbottle.bot import Bot, Message

from vkbottle import Keyboard, Text

bot = Bot(token=TOKEN)

users = [162099941, 320349065]

redis_cl = redis.Redis(host=DB_HOST, port=DB_PORT, db=0, password=DB_PASS)

print(redis_cl.dump("test.rdb"))

bd = BD(redis_cl)

keyboard = Keyboard(one_time=False).add(Text("-> 📌 Личный кабинет", {"profile": "local"})
                            ).row().add(Text("-> ✏ Расписание занятий", {"lessons": "local"})
                            ).row().add(Text("-> 💳 Оплатить", {"payment": "local"})
                            ).row().add(Text("-> ❓ Задать вопрос", {"question": "local"})
                            ).get_json()

@bot.on.message(payload={"profile": "local"})
async def profile(msg: Message):
    await msg.answer(bd.get_profile(msg.from_id), keyboard=keyboard)

@bot.on.message(payload={"lessons": "local"})
async def lessons(msg: Message):
    await msg.answer(bd.get_lessons(msg.from_id), keyboard=keyboard)

@bot.on.message()
async def msg(msg: Message):
    await msg.answer("Привет! 👋🏻\nЧто бы ты хотел узнать? 👀", keyboard=keyboard)

bot.run_forever()