import redis
import time
import datetime
import logging
import json 

from config import DB_HOST, DB_PASS, DB_PORT

class BD:
    def __init__(self) -> None:
        try:
            redis_cl = redis.Redis(host=DB_HOST,
                                   port=DB_PORT,
                                   db=0,
                                   password=DB_PASS)
            redis_cl.ping()
        except:
            print("FATAL ERROR REDIS CONNECTION")
            logging.error("FATAL ERROR REDIS CONNECTION")
            quit()

        self.redis_cl = redis_cl

        print("CONNECTION SUCCESSFUL")
        logging.info("CONNECTION SUCCESSFUL")
    
    def get_payment(self) -> str:
        return self.redis_cl.get("_PaymentInfo").decode('utf-8')
    
    def edit_payment(self, info: str):
        self.redis_cl.set("_PaymentInfo", info)
        return f"Инструкция обнавлена на:\n{info}"

    def get_users(self):
        tmp_str = ""

        for id in self.redis_cl.keys():
            if id == "_PaymentInfo": continue
            try:
                name = json.loads(self.redis_cl.get(id))["name"]
                tmp_str += f"({id.decode('utf-8')}) {name}\n"
            except:
                continue
        
        return tmp_str

    def get_user(self, id: str):
        try:
            id = int(id)
        except:
            return "Не верный id, короче ошибка :/"
        
        if self.redis_cl.exists(id) == 0:
            return "Не верный id, короче ошибка :/"

        data: dict = json.loads(self.redis_cl.get(id))

        tmp_str = f"{id}\n"

        for value in data.values():
            tmp_str += f"{value}\n"

        return tmp_str

    def edit_user(self, info: str):
        try:
            values = str.split(info, "\n")
            id = int(values[0])
            tmp_jsonstr = self.redis_cl.get(id)
        except:
            return "Не верный id/формат строки, короче ошибка :/"

        tmp_json: dict = json.loads(tmp_jsonstr)

        for key, value in zip(tmp_json, values[1:]):
            if value == '/ ': continue
            tmp_json[key] = value
            
        self.redis_cl.set(id, json.dumps(tmp_json))

        return f"Пользователь с айди ({id}) изменен!"
    
    def new_user(self, id: str):
        try:
            id = int(id)
        except:
            return "Не верный id, короче ошибка :/"
        
        tmp_user = {
            "name": "none",
            "age": 0,
            "course": "none",
            "lvl": "none",
            "sex": "none", # М/Ж
            "parent_name": "none",
            "parent_numbet": "none",
            "home_work": "none",

            "lessons_have": 0,
            "lesson": "none"
        }

        user = json.dumps(tmp_user)

        self.redis_cl.set(id, user)

        return f"Пользователь с айди ({id}) создан!"
    
    def get_lessons(self, id: int) -> str:
        data = self.redis_cl.get(id)

        if data == None: return "ERROR :/"

        info = json.loads(data)
        
        l_string = "   ✏ Расписание занятий\n"
        l_number = 1

        for lesson in info["lessons"]:

            time = datetime.datetime.utcfromtimestamp(lesson["time"]).strftime("%d/%m/%Y-%H:%M")
            home_work = "" if lesson["home_work"] == None else lesson["home_work"]
            lesson_paid = "✅" if l_number <= info["lessons_have"] else "❌"

            l_string += f"-> {lesson_paid} {time} - {home_work}\n"
            l_number += 1
        
        l_string += f"Оплачено: {info['lessons_have']} занятия"
        
        return l_string

    def get_lesson(self, id: int) -> str:
        data = self.redis_cl.get(id)

        if data == None: return "ERROR :/"

        info = json.loads(data)

        return f'''О занятиях
-> {info["lesson"]}
-> Домашние задание: {info["home_work"]}
-> Осталось занятий: {"Заморожено" if int(info["lessons_have"]) == -1 else (f"{info['lessons_have']} (Не забудьте оплатить)" if int(info["lessons_have"]) != 0  else info['lessons_have'])}'''
#                   -> Комментарий: {info["comment"]}

    def get_profile(self, id: int) -> str:
        data = self.redis_cl.get(id)

        if data == None: return "ERROR :/"

        info = json.loads(data)
        
        return f'''Личный кабинет
-> Имя ученика: {info['name']}
-> Возраст: {info['age']}
-> Курс: {info['course']}
-> Уровень: {info['lvl']}'''
