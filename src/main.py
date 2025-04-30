"""Entry point of the program."""

from app import App
from mas.examples.tool_testing import test_tool


def main():
    """Entry point of the program."""
    app = App()
    app.run()

    # Test the basic MAS
    test_tool(app)


if __name__ == "__main__":
    main()
