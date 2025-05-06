"""Entry point of the program."""

from app import App
from examples.database_kb import run_database_kb

# from examples.base_model_kb import run_base_model_kb
# from mas.examples.mas_testing import test_basic_mas

#from mas.examples.mas_testing import test_basic_mas
# from mas.examples.recipe_testing import test_recipe_mas

def main():
    """Entry point of the program."""
    app = App()
    app.run()

    # test_basic_mas(app)

    # run_base_model_kb(app)
    run_database_kb(app)
    # test_recipe_mas(app)


if __name__ == "__main__":
    main()
