import importlib.metadata
import sys


def main() -> int:
    version = importlib.metadata.version("grue")

    print(f"\nGrue Z-Machine Interpreter (Version: {version})\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
