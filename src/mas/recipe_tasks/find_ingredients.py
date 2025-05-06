"""Module to run a simple model using Autogen2 to complete a basic task of writing a sentence about a topic."""

from pydantic import BaseModel
from typing import List, Optional
from mas.base_resource import BaseResource
from mas.task import Task

class Ingredient(BaseModel):
    name: str
    measurement: str

class RecipeNameResource(BaseResource):
    class RecipeNameModel(BaseModel):
        """user specifications"""
        recipe_name: str

        def __init__(self, *, recipe_name: str):
            super().__init__(recipe_name=recipe_name)
            self.recipe_name = recipe_name

    def __init__(self, request: RecipeNameModel):
        super().__init__(request)
        self.request = request

    @staticmethod
    def get_model_type() -> type[RecipeNameModel]:
        return RecipeNameResource.RecipeNameModel

class IngredientResource(RecipeNameResource):
    class IngredientModel(BaseModel):
        ingredients: List[Ingredient]

        def __init__(self, *, ingredients: List[Ingredient]):
            super().__init__(ingredients=ingredients)
            self.ingredients = ingredients

    def __init__(self, ingredients: IngredientModel):
        super().__init__(ingredients)
        self.ingredients = ingredients

    @staticmethod
    def get_model_type() -> type[IngredientModel]:
        return IngredientResource.IngredientModel

class FindIngredientsTask(Task[RecipeNameResource, IngredientResource]):
    def _do_work(self, input_resource: RecipeNameResource) -> IngredientResource:

        generated_ingredients = input_resource.response.get("ingredients", [])
        ingredient_list = [Ingredient(**item) for item in generated_ingredients]
        return IngredientResource(IngredientResource.IngredientModel(ingredients=ingredient_list))

    def __init__(self):
        super().__init__(
            "FindIngredientsTask",
            "A task that generates a list of ingredients and their quantities based on a given recipe name.",
            RecipeNameResource.RecipeNameModel,
            IngredientResource.IngredientModel,
            self._do_work,
        )
