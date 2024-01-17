class Handler:
    # класс для управления вводами и взаимодействием с приложением
    def __init__(self, db):
        self.db = db

    # метод добавления предмета
    def update_schedule(self):
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
            elif not self.db.check_teacher(teacher):
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
            try:
                capacity = int(input("Введите вместимость кабинета (или оставьте пустым для автоматического выбора): "))
                if 20 <= capacity <= 30:
                    break
                print("Вместимость наших кабинетов всего от 20 до 30 человек.")
            except ValueError:
                capacity = self.db.get_room_capacity(room)
                break
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
        subjects = self.db.get_subjects()
        print("Выберите предмет для удаления:")
        for i, subject in enumerate(subjects):
            print(f"{i+1}. {subject[1]} (ID: {subject[0]})")
        print(f"{len(subjects)+1}. Ввести ID или название предмета самостоятельно")
        print(f"{len(subjects)+2}. Отменить")
        choice = input("Выберите цифру: ")
        if choice.isdigit() and 1 <= int(choice) <= len(subjects):
            self.db.delete_subject_by_id(subjects[int(choice)-1][0])
        elif choice.isdigit() and int(choice) == len(subjects)+1:
            subject = input("Введите ID или название предмета для удаления: ")
            if subject.isdigit():
                self.db.delete_subject_by_id(int(subject))
            else:
                self.db.delete_subject_by_name(subject)
        elif choice.isdigit() and int(choice) == len(subjects)+2:
            return
        else:
            print("Неправильный выбор, попробуйте еще раз")
        print("Предмет успешно удален.")
