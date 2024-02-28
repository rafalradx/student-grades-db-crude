from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    ForeignKey,
    Text,
    DECIMAL,
    Date,
)
from datetime import datetime

from sqlalchemy.orm import sessionmaker, declarative_base, relationship

engine = create_engine("sqlite:///test.db", echo=False)

# engine = create_engine("postgresql://postgres:123abc@localhost/postgres")

DBSession = sessionmaker(bind=engine)
session = DBSession()
Base = declarative_base()


class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer(), primary_key=True)
    name = Column(String(30), nullable=False)
    students = relationship("Student", back_populates="group")


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer(), primary_key=True)
    name = Column(String(50), nullable=False)
    group_id = Column(Integer(), ForeignKey("groups.id"))
    group = relationship("Group", back_populates="students")
    grades = relationship("Grade", back_populates="student")


class Lecturer(Base):
    __tablename__ = "lecturers"
    id = Column(Integer(), primary_key=True)
    name = Column(String(50), nullable=False)
    subjects = relationship("Subject", back_populates="lecturer")


class Subject(Base):
    __tablename__ = "subjects"
    id = Column(Integer(), primary_key=True)
    name = Column(String(50), nullable=False)
    lecturer_id = Column(Integer(), ForeignKey("lecturers.id"))
    lecturer = relationship("Lecturer", back_populates="subjects")
    grades = relationship("Grade", back_populates="subject")


class Grade(Base):
    __tablename__ = "grades"
    id = Column(Integer(), primary_key=True)
    value = Column(DECIMAL(4, 1), nullable=False)
    student_id = Column(Integer(), ForeignKey("students.id"))
    subject_id = Column(Integer(), ForeignKey("subjects.id"))
    date_of = Column(Date(), nullable=False)
    student = relationship("Student", back_populates="grades")
    subject = relationship("Subject", back_populates="grades")


# backref vs back_populates
# z backref wystarczy tylko raz zdefiniować i mamy relacje obustronną

Base.metadata.create_all(engine)
Base.metadata.bind = engine

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
