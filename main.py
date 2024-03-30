class Student:

    def __init__(self, name: str, surname: str, gender: str) -> None:
        """
        Инициализация класса Student

        :param name: Имя студента
        :param surname: Фамилия студента
        :param gender: Пол студента
        :return: None
        """
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def add_course(self, course_name: str) -> None:
        """
        Добавляет студенту завершенный курс

        :param course_name: Название курса, который завершил студент
        :return: None
        """
        self.finished_courses.append(course_name)

    def rate_mentor(self, lecturer: object, course: str, grade: int) -> None:
        """
        Метод, позволяющий студенту оценить лектора по данному курсу

        :param lecturer: Лектор, которому студент поставит оценку
        :param course: Курс, который ведет лектор
        :param grade: Оценка студента для лектора
        :return: None
        """
        # Проверка, что это лектор, он ведет данный курс и у студента
        # тоже есть данный курс
        if isinstance(lecturer, Lecturer) and (
                course in lecturer.courses_attached) and (
                course in self.courses_in_progress):
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'

    def _average_grade(self) -> float:
        """
        Высчитывает среднюю оценку студента по ВСЕМ курсам.

        :return: Средняя оценка студента
        """
        sum_ = 0
        count = 0
        for course in self.grades.values():  # проход по всем курсам
            for grade in course:  # проход по всем оценкам в курсе
                sum_ += grade
                count += 1
        if count == 0:  # попытка посчитать оценок, если их выставили
            return 'Оценок нет'
        return round(sum_ / count, 1)

    def __gt__(self, other: object) -> bool:
        """
        Перегрузка оператора '>'.
        Сравнивает больше ли средняя оценка студента по всем курсам, по
        сравнению с другим учеником.

        :param other: Другой ученик
        :return: True - оценка больше, False - оценка меньше
        """
        return self._average_grade() > other._average_grade()

    def __str__(self) -> str:
        """
        Перегрузка вывода при вызове print()

        :return: Строка с информацией об учение
        """
        print_return = (f"Имя: {self.name}\n"
                        f"Фамилия: {self.surname}\n"
                        f"Средняя оценка за домашние задания: {
                        self._average_grade()}\n"
                        f"Курсы в процессе изучения: {
                        ', '.join(self.courses_in_progress)}\n"
                        f"Завершенные курсы: {
                        ', '.join(self.finished_courses)}\n")
        return print_return


class Mentor:

    def __init__(self, name: str, surname: str) -> None:
        """
        Инициализация класса Mentor

        :param name: Имя ментора
        :param surname: Фамилия ментора
        """
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):

    def __init__(self, name: str, surname: str) -> None:
        """
        Инициализация класса Lecturer, наследуемый от класса Mentor.

        :param name: Имя лектора
        :param surname: Фамилия лектора
        """
        super().__init__(name, surname)
        self.grades = {}

    def _average_grade(self) -> float:
        """
        Высчитывает среднюю оценку лектора от студентов по ВСЕМ курсам.

        :return: Средняя оценка лектора
        """
        sum_ = 0
        count = 0
        for course in self.grades.values():  # проход по всем курсам
            for grade in course:  # проход по всем оценкам
                sum_ += grade
                count += 1
        if count == 0:  # если у лектора нет оценок
            return 'Оценок нет'
        return round(sum_ / count, 1)

    def __gt__(self, other: object) -> bool:
        """
        Перегрузка оператора '>'.
        Сравнивает больше ли средняя оценка лектора по всем курсам от
        студентов, по сравнению с другим лектором.

        :param other: Другой лектор
        :return: True - оценка больше, False - оценка меньше
        """
        return self._average_grade() > other._average_grade()

    def __str__(self) -> str:
        """
        Перегрузка вывода при вызове print()

        :return: Строка с информацией об лекторе
        """
        print_return = (f"Имя: {self.name}\n"
                        f"Фамилия: {self.surname}\n"
                        f"Средняя оценка за лекции: {
                        self._average_grade()}\n")
        return print_return


class Reviewer(Mentor):

    def __init__(self, name: str, surname: str) -> None:
        """
        Инициализация класса Reviewer, наследуемый от класса Mentor.

        :param name: Имя эксперта
        :param surname: Фамилия эксперта
        """
        super().__init__(name, surname)

    def rate_hw(self, student: object, course: str, grade: int) -> None:
        """
        Метод, позволяющий эксперту оценить домашнее задание студента по
        данному курсу

        :param student: Студент, которому эксперт поставит оценку
        :param course: Курс, по которому будет выставлена оценка
        :param grade: Оценка студента за домашнее задание
        :return: None
        """
        # Проверка, что это студент, что эксперт ведет данный курс и у
        # студента есть данный курс
        if isinstance(student, Student) and (
                course in self.courses_attached) and (
                course in student.courses_in_progress):
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self) -> str:
        """
        Перегрузка вывода при вызове print()

        :return: Строка с информацией об эксперте
        """
        print_return = (f"Имя: {self.name}\n"
                        f"Фамилия: {self.surname}\n")
        return print_return


def students_avg_course_rate(students: list[object], course: str) -> float:
    """
    Функция получает на вход список студентов и выбранный курс.
    Возвращает среднюю оценку по всем студентам по этому курсу.

    :param students: Список студенток класса Student
    :param course: Курс, по которому будет считаться средняя оценка
    :return: Средний оценка по курсу по всем студентам
    """
    sum_ = 0
    count = 0
    for student in students:  # проход по всем студентам
        # проверка, что это студент и у него есть этот курс
        if isinstance(student, Student) and (
                course in student.courses_in_progress):
            if course in student.grades:  # если есть оценки по курсу
                for grade in student.grades[course]:
                    sum_ += grade
                    count += 1
            else:  # если у студента нет оценок
                continue
        else:
            return 'Ошибка'
    if count == 0:  # если нет оценок по данному курсу
        return 'Оценок нет'
    return round(sum_ / count, 1)


def lecturers_avg_course_rate(lecturers: list[object], course: str) -> float:
    """
   Функция получает на вход список лекторов и выбранный курс.
   Возвращает среднюю оценку от студентов по всем лекторам по этому курсу.

   :param lecturers: Список лекторов класса lecturers
   :param course: Курс, по которому будет считаться средняя оценка
   :return: Средний оценка по курсу по всем лекторам
   """
    sum_ = 0
    count = 0
    for lecturer in lecturers:  # проход по всем лекторам
        # проверка, что это лектор и он ведет данный курс
        if isinstance(lecturer, Lecturer) and (
                course in lecturer.courses_attached):
            if course in lecturer.grades:  # если есть оценки по курсу
                for grade in lecturer.grades[course]:
                    sum_ += grade
                    count += 1
            else:  # если у лектора нет оценок по данному курсу
                continue
        else:
            return 'Ошибка'
    if count == 0:  # если нет оценок по данному курсу
        return 'Оценок нет'
    return round(sum_ / count, 1)

# экземпляр первого студент
best_student = Student('Ruoy', 'Eman', 'man')
best_student.courses_in_progress += ['Python', 'Git']
best_student.add_course('Введение в программирование')
# экземпляр второго студента
other_student = Student('Mark', 'Smit', 'man')
other_student.courses_in_progress += ['Python', 'Git']
other_student.add_course('Введение в программирование')
# экземпляр эксперта
cool_reviewer = Reviewer('Some', 'Buddy')
cool_reviewer.courses_attached += ['Python']
# оценки первого студента
cool_reviewer.rate_hw(best_student, 'Python', 8)
cool_reviewer.rate_hw(best_student, 'Python', 9)
cool_reviewer.rate_hw(best_student, 'Python', 9)
# оценки второго студента
cool_reviewer.rate_hw(other_student, 'Python', 10)
cool_reviewer.rate_hw(other_student, 'Python', 9)
cool_reviewer.rate_hw(other_student, 'Python', 9)
# экземпляр первого лектора
cool_lecturer = Lecturer('Oleg', 'Bulygin')
cool_lecturer.courses_attached += ['Python']
# экземпляр второго лектора
other_lecturer = Lecturer('Elena', 'Nikitina')
other_lecturer.courses_attached += ['Python']
# оценки первому лектору
best_student.rate_mentor(cool_lecturer, 'Python', 10)
other_student.rate_mentor(cool_lecturer, 'Python', 10)
# оценки второму лектору
best_student.rate_mentor(other_lecturer, 'Python', 10)
other_student.rate_mentor(other_lecturer, 'Python', 9)
# информация о всех объектах
print(cool_reviewer)
print(cool_lecturer)
print(other_lecturer)
print(best_student)
print(other_student)
# сравнение оценок 2ух студентов и 2ух лекторов
print(best_student > other_student)
print(cool_lecturer > other_lecturer)
# средняя оценка студентов и средняя оценка лекторов
print()
students = [best_student, other_student]
print("Средняя оценка студентов по курсу Python:",
      students_avg_course_rate(students, 'Python'))
lecturers = [cool_lecturer, other_lecturer]
print("Средняя оценка лекторов по курсу Python:",
      lecturers_avg_course_rate(lecturers, 'Python'))
