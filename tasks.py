import sys

from invoke import task

KWARGS = {}
if sys.platform in ["win32", "msys", "cygwin"]:
    KWARGS.update(
        {"pty": False, "encoding": "utf-8", "env": {"PYTHONIOENCODING": "utf-8"}}
    )
else:
    KWARGS.update({"pty": True})


@task
def clean(c):
    print("\n *** Cleaning ***")
    c.run(
        "poetry run python -c \"import pathlib; [p.unlink() for p in pathlib.Path('.').rglob('*.py[co]') if not str(p).startswith('.venv')]\""
    )
    c.run(
        "poetry run python -c \"import pathlib; [p.rmdir() for p in pathlib.Path('.').rglob('__pycache__') if not str(p).startswith('.venv')]\""
    )
    c.run(
        "poetry run python -c \"import shutil; shutil.rmtree('./.pytest_cache', ignore_errors=True)\""
    )
    c.run(
        "poetry run python -c \"import shutil; shutil.rmtree('./.mypy_cache', ignore_errors=True)\""
    )


@task
def formatting(c):
    print("\n*** Formatting (with black) ***")
    c.run("poetry run black src tests", **KWARGS)


@task
def linting(c):
    print("\n*** Linting (with flake8) ***")
    c.run("poetry run flake8 src tests")


@task
def typing(c):
    print("\n*** Typing (with mypy) ***")
    c.run("poetry run mypy src tests")


@task
def testing(c):
    print("\n*** Testing (with pytest) ***")
    c.run("poetry run pytest", **KWARGS)


@task(formatting, linting, typing, testing)
def check(c):
    print("\n QUALITY CHECKS COMPLETED\n")
