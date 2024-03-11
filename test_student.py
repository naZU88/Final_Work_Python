from student import Student

def get_test_student():
    test_student = Student("Анна Иванова", "subjects.csv")
    test_student.add_grade("Физика", 5)
    test_student.add_test_score("Физика", 50)
    return test_student


def test_str():
    test_student = get_test_student()
    assert str(test_student) == 'Студент: Анна Иванов\nПредметы: Физика'

def test_get_average_grade():
    test_student = get_test_student()
    assert test_student.get_average_grade() == 5

def test_average_test_score():
    test_student = get_test_student()
    assert test_student.get_average_test_score("Математика") == 50.0
