from db_models import Group, Lecturer, Student, Subject, Grade
from db_connect import session
from datetime import datetime

# this is for testing purpose only
if __name__ == "__main__":

    group1 = Group(name="truskawki")
    lecturer1 = Lecturer(name="Richard Feynman")
    stud1 = Student(name="Grzegorz Brzeczyszczykiewicz", group=group1)
    stud2 = Student(name="Ferdynand wspanialy", group=group1)
    subj1 = Subject(name="Quantum Field Thoery", lecturer=lecturer1)

    today_date = datetime.today().date()

    grade1 = Grade(value=4.5, student=stud1, subject=subj1, date_of=today_date)
    try:
        session.add_all([group1, lecturer1, subj1])
    except:
        pass

    session.add_all([stud1, stud2, grade1])
    session.commit()

    students = session.query(Student).all()

    for student in students:
        print(student.group.name)

    groups = session.query(Group).all()

    for group in groups:
        for student in group.students:
            print(f"{student.name} is in {group.name}")
