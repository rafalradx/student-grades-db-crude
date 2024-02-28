import argparse

myparser = argparse.ArgumentParser(
    prog="DB manipulator",
    description="CLI to manipulate a database with students, grades, subjects and lecturers",
)
myparser.add_argument(
    "-a",
    "--action",
    type=str,
    choices=["create", "read", "update", "delete", "list", "seed"],
    required=True,
    help="Specify db action",
)
myparser.add_argument(
    "-m",
    "--model",
    type=str,
    choices=["Teacher", "Student", "Group", "Subject", "Grade"],
    required=True,
    help="Specify object type",
)

myparser.add_argument("-n", "--name", type=str, help="name of the object")
myparser.add_argument(
    "-i", "--id", type=int, nargs="+", help="id of an object(s) to take action on"
)

myparser.add_argument(
    "-v",
    "--value",
    type=float,
    choices=[2.0, 3.0, 3.5, 4.0, 4.5, 5.0],
    help="numeric value ",
)

myparser.add_argument("-d", "--date", type=str, help="date in format YYYY-MM-DD")
