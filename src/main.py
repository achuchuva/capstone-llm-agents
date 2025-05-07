"""Entry point of the program."""

from app import App
from mas.examples.comm_test import test_comm_proto_mas


def main():
    """Entry point of the program."""
    app = App()
    app.run()

    test_comm_proto_mas(app)


if __name__ == "__main__":
    main()
