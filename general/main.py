from db.database import Database
from handlers.handlers import Handler

def main():
    # инциализация бд и обработчика
    db = Database()
    handler = Handler(db)
    
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
        if choice == '1':
            if db.schedule_exists():
                handler.update_schedule()
            else:
                handler.create_schedule()
        elif choice == '2' and db.schedule_exists():
            handler.view_schedule()
        elif choice == '3' and db.schedule_exists():
            handler.delete_subject()
        elif choice == '4':
            break
        else:
            print("Неправильный выбор, попробуйте еще раз")

if __name__ == "__main__":
    main()