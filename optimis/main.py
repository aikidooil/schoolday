from db.database import Database
from handlers.handlers import Handler

def main():
    # инциализация бд и обработчика
    db = Database()
    handler = Handler(db)
    # если в базе данных есть расписание
    menu = {
        '1': ('Обновить расписание', handler.update_schedule),
        '2': ('Посмотреть сегодняшнее расписание', handler.view_schedule),
        '3': ('Удалить предмет из расписания', handler.delete_subject),
        '4': ('Выйти', exit)
    }
    while True:
        print("\n1. Создать расписание" if not db.schedule_exists() else "\n".join(f"{k}. {v[0]}" for k, v in menu.items()))
        choice = input("Выберите цифру: ")
        if choice in menu and (choice != '2' and choice != '3' or db.schedule_exists()):
            menu[choice][1]()
        else:
            print("Неправильный выбор, попробуйте еще раз")

if __name__ == "__main__":
    main()
