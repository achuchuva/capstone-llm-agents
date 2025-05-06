"""Entry point of the program."""

from app import App
#from mas.examples.mas_testing import test_basic_mas
from mas.examples.recipe_testing import recipe_agent_mas

def main():
    """Entry point of the program."""
    app = App()
    app.run()

    recipe_agent_mas(app)


if __name__ == "__main__":
    main()
