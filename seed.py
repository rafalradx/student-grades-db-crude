from db_models import session, Group, Lecturer, Student, Subject, Grade

import faker
from random import randint, choice
from datetime import date, timedelta

NUMBER_STUDENTS = 40

GROUPS = ["BT-102", "BCh-202", "BPh-301"]
NUMBER_GROUPS = len(GROUPS)

GRADES = [2.0, 3.0, 3.5, 4.0, 4.5, 5.0]

SUBJECTS = [
    "General relativity",
    "Quantum electro-dynamics",
    "Probability Theory",
    "Introduction to Magnetic Resonance",
    "Protein Structure",
    "Nuclear Fusion",
    "Calculus",
    "Stochastic Processes",
]
NUMBER_SUBJECTS = len(SUBJECTS)

LECTURERS = [
    "prof. Richard Feynman",
    "prof. Erwin Hahn",
    "prof. Paul Dirac",
    "prof. John von Neumann",
    "prof. Paul Langevin",
]
NUMBER_LECTURERS = len(LECTURERS)

NUMBER_GRADES_PER_STUDENT = 15
NUMBER_GRADES = NUMBER_STUDENTS * NUMBER_SUBJECTS * NUMBER_GRADES_PER_STUDENT

START_DATE = "2023-09-01"
END_DATE = "2024-02-10"


def generate_fake_data(number_students) -> tuple:
    fake_students = []
    fake_data = faker.Faker()

    for _ in range(number_students):
        fake_students.append(fake_data.name())

    return fake_students


def random_date(start_date, end_date):
    start_date = date(*map(int, start_date.split("-")))
    end_date = date(*map(int, end_date.split("-")))

    delta = end_date - start_date
    random_days = randint(0, delta.days)
    random_date = start_date + timedelta(random_days)
    return random_date


def main(*arg):
    fake_students_names = generate_fake_data(NUMBER_STUDENTS)
    groups_to_db = [Group(name=group) for group in GROUPS]
    lecturers_to_db = [Lecturer(name=lecturer) for lecturer in LECTURERS]
    students_to_db = [
        Student(name=fake_name, group=choice(groups_to_db))
        for fake_name in fake_students_names
    ]
    subjects_to_db = [
        Subject(name=subject_name, lecturer=choice(lecturers_to_db))
        for subject_name in SUBJECTS
    ]

    grades_to_db = []

    for subject in subjects_to_db:
        for _ in range(NUMBER_GRADES_PER_STUDENT):
            when_date = random_date(START_DATE, END_DATE)
            for student in students_to_db:
                grades_to_db.append(
                    Grade(
                        value=choice(GRADES),
                        student=student,
                        subject=subject,
                        date_of=when_date,
                    )
                )

    session.add_all(
        groups_to_db + lecturers_to_db + students_to_db + subjects_to_db + grades_to_db
    )
    session.commit()


if __name__ == "__main__":
    main()
