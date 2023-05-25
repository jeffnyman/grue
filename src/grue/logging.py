import os


def setup_logging(filename: str) -> None:
    if os.path.exists(filename):
        with open(filename, "w"):
            pass


def log(message: str) -> None:
    with open("log.txt", "a") as logfile:
        print(message, file=logfile)
