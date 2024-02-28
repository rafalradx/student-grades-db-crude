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

# engine = create_engine("sqlite:///test.db", echo=False)

engine = create_engine("postgresql://postgres:123abc@localhost:5432/postgres")

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


Base.metadata.create_all(engine)
Base.metadata.bind = engine
