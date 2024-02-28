from db_models import session, Group, Lecturer, Student, Subject, Grade
from sqlalchemy import func, desc


# Znajdź 5 studentów z najwyższą średnią ocen ze wszystkich przedmiotów.
def select_1():
    results = (
        session.query(
            Student.name, func.round(func.avg(Grade.value), 3).label("avg_grade")
        )
        .join(Student)
        .group_by(Student.id)
        .order_by(desc("avg_grade"))
        .limit(5)
    )
    for res in results:
        print(res.name, res.avg_grade)


# Znajdź studenta z najwyższą średnią ocen z określonego przedmiotu.
def select_2(id):
    results = (
        session.query(
            Student.name, func.round(func.avg(Grade.value), 3).label("avg_grade")
        )
        .join(Student)
        .where(Grade.subject_id == id)
        .group_by(Student.id)
        .order_by(desc("avg_grade"))
        .limit(1)
    )
    for res in results:
        print(res.name, res.avg_grade)


# Znajdź średni wynik w grupach dla określonego przedmiotu.
def select_3(id):
    results = (
        session.query(
            Group.name, func.round(func.avg(Grade.value), 3).label("avg_grade")
        )
        .select_from(Grade)
        .join(Student)
        .join(Group)
        .where(Grade.subject_id == id)
        .group_by(Group.id)
        .order_by(desc("avg_grade"))
    )
    for res in results:
        print(res.name, res.avg_grade)


# Znajdź średni wynik w grupie (w całej tabeli ocen).
def select_4():
    results = (
        session.query(
            Group.name, func.round(func.avg(Grade.value), 3).label("avg_grade")
        )
        .select_from(Grade)
        .join(Student)
        .join(Group)
        .group_by(Group.id)
    )
    for res in results:
        print(res.name, res.avg_grade)


# Znajdź przedmioty, których uczy określony wykładowca.
def select_5(id):
    # Korzystam ze zdefiniowanego relationship backpopulates
    lecturer = session.query(Lecturer).filter_by(id=id).one()
    print(f"Subject taught by: {lecturer.name}:")
    for subject in lecturer.subjects:
        print(subject.name)


# Znajdź listę studentów w określonej grupie.
def select_6(id):
    group = session.query(Group).filter_by(id=id).one()
    print(f"Students in '{group.name}' group:")
    for student in group.students:
        print(student.name)


# Znajdź oceny studentów w określonej grupie z danego przedmiotu.
def select_7(gr_id, subj_id):
    grades = (
        session.query(Grade).filter_by(subject_id=subj_id).order_by(Grade.student_id)
    )
    filtred_grades = filter(lambda grade: grade.student.group_id == gr_id, grades)
    for grade in filtred_grades:
        print(grade.value, grade.student.name, grade.student.group.name)


# Znajdź średnią ocenę wystawioną przez określonego wykładowcę z jego przedmiotów.
def select_8(id):
    results = (
        session.query(
            Lecturer.name,
            Subject.name,
            func.round(func.avg(Grade.value), 3).label("avg_grade"),
        )
        .select_from(Grade)
        .join(Subject)
        .join(Lecturer)
        .where(Lecturer.id == id)
        .group_by(Subject.id)
    )
    for res in results:
        print(res)


# Znajdź listę przedmiotów zaliczonych przez danego studenta.
# Co to znaczy?
def select_9():
    pass


# Znajdź listę kursów prowadzonych przez określonego wykładowcę dla określonego studenta
def select_10(stud_id, lect_id):
    results = (
        session.query(Subject.name)
        .select_from(Grade)
        .join(Student)
        .join(Subject)
        .join(Lecturer)
        .where(Student.id == stud_id)
        .where(Lecturer.id == lect_id)
        .distinct()
    )
    for subj in results:
        print(subj.name)


# Średnia ocena, jaką określony wykładowca wystawił pewnemu studentowi.
def select_11(stud_id, lect_id):
    results = (
        session.query(
            func.round(func.avg(Grade.value), 3).label("avg_grade"),
            Student.name.label("student"),
            Lecturer.name.label("lecturer"),
        )
        .select_from(Grade)
        .join(Student)
        .join(Subject)
        .join(Lecturer)
        .where(Student.id == stud_id)
        .where(Lecturer.id == lect_id)
    )
    for res in results:
        print(
            f"avr. grade = {res.avg_grade} given to: {res.student} by: {res.lecturer}"
        )


# Oceny studentów w określonej grupie z określonego przedmiotu na ostatnich zajęciach.
def select_12(gr_id, subj_id):
    # Number of students in selected group
    res = (
        session.query(func.count(Student.id).label("counter"))
        .where(Student.group_id == gr_id)
        .one()
    )
    how_many = res.counter

    results = (
        session.query(
            Grade.value.label("grade"),
            Grade.date_of.label("date"),
        )
        .select_from(Grade)
        .join(Student)
        .join(Subject)
        .join(Group)
        .where(Subject.id == subj_id)
        .where(Group.id == gr_id)
        .order_by(desc("date"))
        .limit(how_many)
    )

    for res in results:
        print(f"grade = {res.grade} given on: {res.date}")


if __name__ == "__main__":
    select_1()
    select_2(1)
    select_3(8)
    select_4()
    select_5(1)
    select_6(1)
    select_7(1, 3)
    select_8(3)
    select_9()
    select_10(8, 3)
    select_11(2, 2)
    select_12(2, 4)
