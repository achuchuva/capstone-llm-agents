"""Recipe"""

# from app import App

from config.config_manager import ConfigManager
from mas.ag2.ag2_agent import AG2MASAgent
from mas.ag2.ag2_task import AG2Task
from mas.multi_agent_system import MultiAgentSystem
from mas.query.mas_query import MASQuery
from mas.resource_alias import ResourceAlias
from mas.resources.empty import EmptyResource
from mas.recipe_tasks.find_recipe import UserRequestResource, RecipeResource
from utils.string_template import generate_str_using_template


def recipe_agent_mas():
    """put description here ig"""

    alias = ResourceAlias()

    alias.add_resource_alias("empty", EmptyResource)
    alias.add_resource_alias("recipe", RecipeResource)
    alias.add_resource_alias("user_request", UserRequestResource)

    mas = MultiAgentSystem(alias)

    config_manager = ConfigManager("./config/app.json")

    mas_query = MASQuery.from_yaml("./resource/examples/recipe.yaml")

    print("mas_query:")
    print(mas_query)

    agent = AG2MASAgent(
        name="RecipeAgent",
        description="You are a recipe generation assistant.",
        llm_config=config_manager.get_llm_config(use_tools=False),
    )

    find_recipe_task = AG2Task(
        name="FindRecipeTask",
        description="Generate a recipe name based on the user's preferences.",
        input_resource=UserRequestResource,
        output_resource=RecipeResource,
        generate_str=generate_str_using_template(
            "Generate a recipe name conforming to the following specifications: '{request}'"
        ),
        agent=agent,
    )

    mas.add_task(find_recipe_task)

    output_resources = mas.solve_query(
        mas_query,
        {},
    )

    print("Output:")
    for output_resource in output_resources:
        print(output_resource.model.model_dump_json(indent=4, exclude_unset=True))
