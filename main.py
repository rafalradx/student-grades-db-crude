from myparser import myparser
from db_models import session, Group, Lecturer, Student, Subject, Grade
from argparse import Namespace
from datetime import date

MODELS_MAP = {
    "Group": Group,
    "Teacher": Lecturer,
    "Student": Student,
    "Subject": Subject,
    "Grade": Grade,
}


def create(args: Namespace) -> None:
    model = args.model
    if model == "Group":
        group = Group(name=args.name)
        session.add(group)
        session.commit()
        return
    if model == "Student":
        group_ID = args.id[0]
        student = Student(name=args.name, group_id=group_ID)
        session.add(student)
        session.commit()
        return
    if model == "Teacher":
        group_ID = args.id[0]
        lecturer = Lecturer(name=args.name)
        session.add(lecturer)
        session.commit()
        return
    if model == "Subject":
        lecturer_ID = args.id[0]
        subject = Subject(name=args.name, lecturer_id=lecturer_ID)
        session.add(subject)
        session.commit()
    if model == "Grade":
        student_ID = args.id[0]
        subject_ID = args.id[1]
        date_of_grade = args.date
        date_of = date(*map(int, date_of_grade.split("-")))
        grade = Grade(
            value=args.value,
            student_id=student_ID,
            subject_id=subject_ID,
            date_of=date_of,
        )
        session.add(grade)
        session.commit()


def delete(args: Namespace) -> None:
    record = session.get(MODELS_MAP[args.model], args.id[0])
    session.delete(record)
    session.commit()


def list_all(args: Namespace) -> None:
    results = session.query(MODELS_MAP[args.model]).all()
    for res in results:
        print(res.name)


def read(args: Namespace) -> None:
    record = session.get(MODELS_MAP[args.model], args.id[0])
    print(record.name)


def update(args: Namespace) -> None:
    """Supports changing names only"""
    record = session.get(MODELS_MAP[args.model], args.id[0])
    if args.name is None:
        print("Please provide a new name with -n/--name parameter")
        return
    record.name = args.name
    session.add(record)
    session.commit()


ACTIONS_MAP = {
    "create": create,
    "read": read,
    "update": update,
    "delete": delete,
    "list": list_all,
}

if __name__ == "__main__":
    myargs = myparser.parse_args()
    print(myargs)
    ACTIONS_MAP[myargs.action](myargs)
