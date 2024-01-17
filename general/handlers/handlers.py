class Handler:
    # класс для управления вводами и взаимодействием с приложением
    def __init__(self, db):
        self.db = db

    # метод для проверки ввода пользователя
    def check_input(self, choice, length):
        return choice.isdigit() and 1 <= int(choice) <= length

    # метод добавления предмета
    def update_schedule(self):
        date = self.db.get_today_date()
        schedules = self.db.get_schedules()
        print("Выберите расписание для обновления:")
        for i, schedule in enumerate(schedules):
            print(f"{i+1}. Расписание за {schedule[0]}")
        
        # если расписание уже создано то создать новое можно только завтра
        if date not in [schedule[0] for schedule in schedules]:
            print(f"{len(schedules)+1}. Создать новое расписание")
        
        choice = input("Выберите цифру: ")
        if self.check_input(choice, len(schedules)):
            date = schedules[int(choice)-1][0]
        elif self.check_input(choice, len(schedules)+1) and date not in [schedule[0] for schedule in schedules]:
            pass
        else:
            print("Неправильный выбор, попробуйте еще раз")
            return
        self.add_subject(date)

    # метод создания расписания
    def create_schedule(self):
        date = self.db.get_today_date()
        self.add_subject(date)

    # метод добавления предмета
    def add_subject(self, date):
        while True:
            print("Выберите предмет:\n1. Математика\n2. Английский язык\n3. Информатика\n4. Вписать свой\n5. Отменить")
            choice = input("Выберите цифру: ")
            if choice == '1':
                name = "Математика"
                break
            elif choice == '2':
                name = "Английский язык"
                break
            elif choice == '3':
                name = "Информатика"
                break
            elif choice == '4':
                name = input("Введите название предмета: ")
                if name.isalpha():
                    break
                print("Название предмета должно состоять из букв.")
            elif choice == '5':
                return
            else:
                print("Неправильный выбор, попробуйте еще раз")
        while True:
            teacher = input("Введите преподавателя: ")
            if not teacher.isalpha():
                print("Имя преподавателя должно состоять только из букв.")
            elif not self.db.check_teacher(teacher, date):
                print("Преподаватель может провести до 5 уроков в день.")
            else:
                break
        while True:
            try:
                room = int(input("Введите кабинет: "))
                if 1 <= room <= 150:
                    break
                print("В нашем учебном заведении всего 150 кабинетов.")
            except ValueError:
                print("Неправильный ввод: кабинет должен быть цифрой.")
        while True:
            capacity_input = input("Введите вместимость кабинета (или оставьте пустым для автоматического выбора): ")
            if capacity_input == '':
                capacity = self.db.get_room_capacity(room)
                break
            elif capacity_input.isdigit():
                capacity = int(capacity_input)
                if 20 <= capacity <= 30:
                    break
                print("Вместимость наших кабинетов всего от 20 до 30 человек.")
            else:
                print("Неправильный ввод: вместимость кабинета должна быть числом.")
        self.db.insert_subject(name, teacher, room, capacity, date)
        print("Расписание успешно обновлено.")

    # метод для показа расписания
    def view_schedule(self):
        dates = self.db.get_dates()
        print("Выберите дату расписания:")
        for i, date in enumerate(dates):
            print(f"{i+1}. Расписание за {date[0]}")
        print(f"{len(dates)+1}. Введите дату расписания самостоятельно")
        choice = input("Выберите цифру: ")
        if self.check_input(choice, len(dates)):
            date = dates[int(choice)-1][0]
        elif self.check_input(choice, len(dates)+1):
            date = input("Введите дату расписания (формат YYYY-MM-DD): ")
        else:
            print("Неправильный выбор, попробуйте еще раз")
            return
        subjects = self.db.get_subjects(date)
        print(f"\nРасписание за {date}:")
        for subject in subjects:
            print(f"Предмет: {subject[1]}, Преподаватель: {subject[2]}, Кабинет: {subject[3]}, Вместимость кабинета: {subject[4]}")

    # метод для удаления предмета
    def delete_subject(self):
        while True:
            dates = self.db.get_dates()
            if not dates:
                print("Все предметы удалены.")
                break
            print("Выберите дату расписания:")
            for i, date in enumerate(dates):
                print(f"{i+1}. Расписание за {date[0]}")
            print(f"{len(dates)+1}. Введите дату расписания самостоятельно")
            choice = input("Выберите цифру: ")
            if self.check_input(choice, len(dates)):
                date = dates[int(choice)-1][0]
            elif self.check_input(choice, len(dates)+1):
                date = input("Введите дату расписания (формат YYYY-MM-DD): ")
            else:
                print("Неправильный выбор, попробуйте еще раз")
                continue
            while True:
                subjects = self.db.get_subjects(date)
                if not subjects:
                    print("Все предметы за эту дату удалены.")
                    break
                print("Выберите предмет для удаления:")
                for i, subject in enumerate(subjects):
                    print(f"{i+1}. {subject[1]} (ID: {subject[0]})")
                print(f"{len(subjects)+1}. Ввести ID или название предмета самостоятельно")
                print(f"{len(subjects)+2}. Отменить")
                choice = input("Выберите цифру: ")
                if self.check_input(choice, len(subjects)):
                    self.db.delete_subject_by_id(subjects[int(choice)-1][0])
                elif self.check_input(choice, len(subjects)+1):
                    subject = input("Введите ID или название предмета для удаления: ")
                    if subject.isdigit():
                        self.db.delete_subject_by_id(int(subject))
                    else:
                        self.db.delete_subject_by_name(subject)
                elif self.check_input(choice, len(subjects)+2):
                    return
                else:
                    print("Неправильный выбор, попробуйте еще раз")
                print("Предмет успешно удален.")