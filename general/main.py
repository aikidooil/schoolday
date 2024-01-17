from db.database import Database
from handlers.handlers import Handler

def main():
    # инциализация бд и обработчика
    db = Database()
    handler = Handler(db)
    
    # словарь действий
    actions = {
        '1': lambda: handler.update_schedule() if db.schedule_exists() else handler.create_schedule(),
        '2': handler.view_schedule,
        '3': handler.delete_subject,
        '4': exit
    }
    
    while True:
        # если в базе данных есть расписание
        if db.schedule_exists():
            print("\n1. Обновить расписание")
            print("2. Посмотреть расписание")
            print("3. Удалить предмет из расписания")
            print("4. Выйти")
        else:
            print("\n1. Создать расписание")
            print("4. Выйти")
        choice = input("Выберите цифру: ")
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Неправильный выбор, попробуйте еще раз")

if __name__ == "__main__":
    main()