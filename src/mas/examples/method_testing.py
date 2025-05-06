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
from mas.recipe_tasks.find_method import DataResource, MethodResource
from mas.recipe_tasks.find_ingredients import Ingredient
from utils.string_template import generate_str_using_template

def method_agent_mas(app: App):
    """put description here ig"""

    alias = ResourceAlias()

    alias.add_resource_alias("empty", EmptyResource)
    alias.add_resource_alias("recipe", MethodResource)
    alias.add_resource_alias("user_request", DataResource)

    mas = MultiAgentSystem(alias)

    mas_query = MASQuery.from_yaml("./resource/example/method.yaml")

    print("MAS Query:")
    print(mas_query)

    agent = AG2MASAgent(
        name="RecipeAgent",
        description="You are a recipe method generation assistant.",
        llm_config=app.config_manager.get_llm_config(use_tools=False),
    )

    find_method_task = AG2Task(
        name="FindMethodTask",
        description="Generate a recipe method based on a given recipe name, its ingredients and quantity of each ingredient.",
        input_resource=DataResource,
        output_resource=MethodResource,
        generate_str=generate_str_using_template(
            "Generate a detailed recipe method using the following ingredients and their quantities for the recipe, '{recipe_name}':\n"
            "{ingredient_list}\n"
            "The method should include cooking instructions, techniques, and ingredient usage. Return the method in plain text."
        ),
        agent=agent,
    )

    mas.add_task(find_method_task)


    output_resources = mas.solve_query(mas_query, {}, )

    for output_resource in output_resources:
        print(output_resource.model.model_dump_json(indent=4, exclude_unset=True))