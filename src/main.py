"""Entry point of the program."""

from app import App
from mas.examples.trip import trip_app


def main():
    """Entry point of the program."""
    app = App()
    app.run()

    trip_app(app)


if __name__ == "__main__":
    main()
