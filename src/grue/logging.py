"""Logging module for Grue."""

import os


def setup_logging(filename: str) -> None:
    """Set up a new log by truncating any existing log file."""

    if os.path.exists(filename):
        with open(filename, "w"):
            pass


def log(message: str) -> None:
    """Write a log statement to an existing log file."""

    with open("log.txt", "a") as logfile:
        print(message, file=logfile)


def log_opcode(message: str) -> None:
    with open("log_opcodes.txt", "a") as logfile:
        print(message, file=logfile)
