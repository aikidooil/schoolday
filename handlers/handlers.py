class Handler:
    # класс для управления вводами и взаимодействием с приложением
    def __init__(self, db):
        self.db = db

    # метод добавления предмета
    def update_schedule(self):
        while True:
            print("Выберите предмет:\n1. Математика\n2. Английский язык\n3. Информатика\n4. Вписать свой")
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
            else:
                print("Неправильный выбор, попробуйте еще раз")
        while True:
            teacher = input("Введите преподавателя: ")
            if teacher.isalpha() and self.db.check_teacher(teacher):
                break
            print("Имя преподавателя должно состоять из букв и преподаватель может провести до 5 уроков в день.")
        while True:
            try:
                room = int(input("Введите кабинет: "))
                if 1 <= room <= 150:
                    break
                print("В нашем учебном заведении всего 150 кабинетов.")
            except ValueError:
                print("Неправильный ввод: кабинет должен быть цифрой.")
        while True:
            try:
                capacity = int(input("Введите вместимость кабинета: "))
                if 1 <= capacity <= 30:
                    break
                print("Вместимость наших кабинетов всего 30 человек.")
            except ValueError:
                print("Неправильный ввод: вместимость кабинета должна быть цифрой.")
        self.db.insert_subject(name, teacher, room, capacity)
        print("Расписание успешно обновлено.")

    # метод для показа расписания
    def view_schedule(self):
        subjects = self.db.get_subjects()
        print("\nСегодняшнее расписание:")
        for subject in subjects:
            print(f"Предмет: {subject[1]}, Преподаватель: {subject[2]}, Кабинет: {subject[3]}, Вместимость кабинета: {subject[4]}")

    # метод для удаления предмета
    def delete_subject(self):
        subject = input("Введите ID или название предмета для удаления: ")
        if subject.isdigit():
            self.db.delete_subject_by_id(int(subject))
        else:
            self.db.delete_subject_by_name(subject)
        print("Предмет успешно удален.")
