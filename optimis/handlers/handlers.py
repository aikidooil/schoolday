class Handler:
    def __init__(self, db):
        self.db = db
        self.subjects = {
            '1': 'Математика',
            '2': 'Английский язык',
            '3': 'Информатика',
            '4': self.get_custom_subject,
            '5': exit
        }

    def get_custom_subject(self):
        while True:
            name = input("Введите название предмета: ")
            if name.isalpha():
                return name
            print("Название предмета должно состоять из букв.")

    def get_teacher(self):
        while True:
            teacher = input("Введите преподавателя: ")
            if teacher.isalpha() and self.db.check_teacher(teacher):
                return teacher
            print("Имя преподавателя должно состоять из букв и преподаватель может провести до 5 уроков в день.")

    def get_room(self):
        while True:
            try:
                room = int(input("Введите кабинет: "))
                if 1 <= room <= 150:
                    return room
                print("В нашем учебном заведении всего 150 кабинетов.")
            except ValueError:
                print("Неправильный ввод: кабинет должен быть цифрой.")

    def get_capacity(self, room):
        while True:
            try:
                capacity = int(input("Введите вместимость кабинета (или оставьте пустым для автоматического выбора): "))
                if 20 <= capacity <= 30:
                    return capacity
                print("Вместимость наших кабинетов всего от 20 до 30 человек.")
            except ValueError:
                return self.db.get_room_capacity(room)

    def update_schedule(self):
        while True:
            print("Выберите предмет:\n1. Математика\n2. Английский язык\n3. Информатика\n4. Вписать свой\n5. Отменить")
            choice = input("Выберите цифру: ")
            if choice in self.subjects:
                name = self.subjects[choice]() if callable(self.subjects[choice]) else self.subjects[choice]
                teacher = self.get_teacher()
                room = self.get_room()
                capacity = self.get_capacity(room)
                self.db.insert_subject(name, teacher, room, capacity)
                print("Расписание успешно обновлено.")
                return
            print("Неправильный выбор, попробуйте еще раз")

    def view_schedule(self):
        subjects = self.db.get_subjects()
        print("\nСегодняшнее расписание:")
        for subject in subjects:
            print(f"Предмет: {subject[1]}, Преподаватель: {subject[2]}, Кабинет: {subject[3]}, Вместимость кабинета: {subject[4]}\n")

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
