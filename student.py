#Взять класс студент из дз 12-го семинара, добавить запуск из командной строки(передача в качестве аргумента название 
#csv-файла с предметами), логирование и написать 3-5 тестов с использованием pytest.

import csv
import argparse
import logging

logging.basicConfig(filename='project.log', encoding='utf-8', level=logging.DEBUG)
logger = logging.getLogger()

class Checking:

	def __set_name__(self, owner, name):
		self.name = '_' + name
		

	def __get__(self, instance, owner):
		return getattr(instance, self.name)


	def __set__(self, instance, value):
		self.validate(value)
		setattr(instance, self.name, value)


	def __delete__(self, instance):
		raise AttributeError(f'Свойство "{self.name}" нельзя удалять')


	def validate(self, value):
          if not value.istitle() or value.isalpha():
            logger.error("ФИО должно состоять только из букв и начинаться с заглавной буквы")
            raise ValueError('ФИО должно состоять только из букв и начинаться с заглавной буквы')



class Student:
    name = Checking()

    def __init__(self, name, subjects_file):
        self.name = name
        self.subjects = {}
        self.load_subjects(subjects_file)
		

    def __setattr__(self, name, value):
        if name == "name":
            if not value.istitle() or value.isalpha():
                logger.error("ФИО должно состоять только из букв и начинаться с заглавной буквы")
                raise ValueError('ФИО должно состоять только из букв и начинаться с заглавной буквы')
        object.__setattr__(self, name, value)


    def __getattr__(self, name):
        return f"{self.name}"


    def __str__(self):
        subj = list(filter(lambda x: len(self.subjects[x]['grade']) > 0, self.subjects.keys()))
        return f'Студент: {self.name}\nПредметы: {", ".join(subj)}'


    def load_subjects(self, subjects_file):
        with open(subjects_file, encoding="utf8", newline='\n') as f:
            csv_reader = csv.reader(f, delimiter=' ', quotechar=',')
            for line in csv_reader:
                self.subjects = {subject: {'grade': [], 'test_grade': [], } for subject in line[0].split(',')}


    def add_grade(self, subject, grade):
        if 5 >= grade >= 2:
            if subject in self.subjects.keys():
                self.subjects[subject]['grade'].append(grade)
            else:
                logger.error(f'Предмет {subject} не найден')
                raise ValueError(f'Предмет {subject} не найден')
        else:
            logger.error("Оценка должна быть целым числом от 2 до 5")
            raise ValueError("Оценка должна быть целым числом от 2 до 5")


    def add_test_score(self, subject, test_grade):
        if 100 >= test_grade > 0:
            self.subjects[subject]['test_grade'].append(test_grade)
        else:
            logger.error("Результат теста должен быть целым числом от 0 до 100")
            raise ValueError("Результат теста должен быть целым числом от 0 до 100")


    def get_average_test_score(self, subject):
        if subject in self.subjects.keys() and len(self.subjects[subject]['test_grade']) > 0:
                return sum(self.subjects[subject]['test_grade'])/len(self.subjects[subject]['test_grade'])
        else:
            logger.error(f'Предмет {subject} не найден')
            raise ValueError(f'Предмет {subject} не найден')


    def get_average_grade(self):
        av_list = []
        for subject in self.subjects.keys():
            if len(self.subjects[subject]['grade']) > 0:
                av_list.append(sum(self.subjects[subject]['grade'])/len(self.subjects[subject]['grade']))
        av_list = list(filter(lambda x: x is not None, av_list))
        if len(av_list) > 0:
            return sum(av_list)/len(av_list)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='My first argument parser')
    parser.add_argument('file', metavar='N', type=str, nargs='*', help='press some filename')
    args = parser.parse_args()
    logger.info(f'Получили экземпляр: {args = }')
    if args.file:
        file_csv = args.file[0]
    else:
        file_csv = "subjects.csv"
        logger.info(f'Аргументы не переданы(имя файла по умолчанию): {file_csv}')

    # student = Student("Иван Иванов", "subjects.csv")

    # student.add_grade("Математика", 4)
    # student.add_test_score("Математика", 85)

    # student.add_grade("История", 5)
    # student.add_test_score("История", 92)

    # average_grade = student.get_average_grade()
    # print(f"Средний балл: {average_grade}")

    # average_test_score = student.get_average_test_score("Математика")
    # print(f"Средний результат по тестам по математике: {average_test_score}")

    # print(student)