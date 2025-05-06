"""Recipe"""

# from app import App

from app import App
from config.config_manager import ConfigManager
from mas.ag2.ag2_agent import AG2MASAgent
from mas.ag2.ag2_task import AG2Task
from mas.multi_agent_system import MultiAgentSystem
from mas.query.mas_query import MASQuery
from mas.resource_alias import ResourceAlias
from mas.resources.empty import EmptyResource
from mas.recipe_tasks.find_ingredients import RecipeNameResource, IngredientResource, Ingredient
from utils.string_template import generate_str_using_template


def ingredient_agent_mas(app: App):
    """put description here ig"""

    alias = ResourceAlias()

    alias.add_resource_alias("empty", EmptyResource)
    alias.add_resource_alias("recipe", IngredientResource)
    alias.add_resource_alias("user_request", RecipeNameResource)

    mas = MultiAgentSystem(alias)

    mas_query = MASQuery.from_yaml("./resource/example/ingredients.yaml")

    print("MAS Query:")
    print(mas_query)

    agent = AG2MASAgent(
        name="RecipeAgent",
        description="You are a recipe ingredients generation assistant.",
        llm_config=app.config_manager.get_llm_config(use_tools=False),
    )

    find_ingredients_task = AG2Task(
        name="FindRecipeTask",
        description="Generate a list of ingredients and their quantities based on a given recipe name.",
        input_resource=RecipeNameResource,
        output_resource=IngredientResource,
        generate_str=generate_str_using_template(
            "Generate a list of ingredients and their measurements for the given recipe, '{recipe_name}'. "
            "Each ingredient must be returned as a dictionary with 'name' and 'measurement' fields. "
            "Only return a JSON array of these ingredients, absolutely nothing else."
        ),
        agent=agent,
    )

    mas.add_task(find_ingredients_task)

    output_resources = mas.solve_query(mas_query, {}, )

    for output_resource in output_resources:
        if isinstance(output_resource, IngredientResource):
            ingredients = output_resource.ingredients.ingredients 
            print(ingredients)