from myparser import myparser
from db_models import Group, Lecturer, Student, Subject, Grade
from db_connect import session
from argparse import Namespace
from datetime import date
from seed import main

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
        obj = Group(name=args.name)
    elif model == "Student":
        group_ID = args.id[0]
        obj = Student(name=args.name, group_id=group_ID)
    elif model == "Teacher":
        group_ID = args.id[0]
        obj = Lecturer(name=args.name)
    elif model == "Subject":
        lecturer_ID = args.id[0]
        obj = Subject(name=args.name, lecturer_id=lecturer_ID)
    elif model == "Grade":
        student_ID = args.id[0]
        subject_ID = args.id[1]
        date_of_grade = args.date
        date_of = date(*map(int, date_of_grade.split("-")))
        obj = Grade(
            value=args.value,
            student_id=student_ID,
            subject_id=subject_ID,
            date_of=date_of,
        )
    session.add(obj)
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
    "seed": main,
}

if __name__ == "__main__":
    myargs = myparser.parse_args()
    ACTIONS_MAP[myargs.action](myargs)
