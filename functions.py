import redis

class BD:
    def __init__(self, redis = None) -> None:
        print(redis)
        pass
    
    def get_lessons(self, id: int) -> str:
        lessons = []
        pass

    def get_profile(self, id: int) -> str:
        info = "test_info"
        return (f"-> Имя ученика: {info}" # Николай
            f"\n-> Возраст: {info}" # 13
            f"\n-> Курс: {info}" # Scratch/Construct/Godot
            f"\n-> Уровень: {info}" # Начальный
            f"\n-> Комментарии: {info}")