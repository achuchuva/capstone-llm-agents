"""Module to run a simple model using Autogen2 to complete a basic task of writing a sentence about a topic."""

from pydantic import BaseModel
from typing import List, Dict, Optional
from mas.base_resource import BaseResource
#from mas.recipe_tasks.find_ingredients import Ingredient
from mas.task import Task


class DataResource(BaseResource):
    class DataModel(BaseModel):
        """user specifications"""
        recipe_name: str
        ingredient_list: List[Dict[str, str]]

        def __init__(self, *, recipe_name: str, ingredient_list: List[Dict[str, str]]):
            super().__init__(recipe_name=recipe_name, ingredient_list=ingredient_list)
            self.recipe_name = recipe_name
            self.ingredient_list = ingredient_list

    def __init__(self, request: DataModel):
        super().__init__(request)
        self.request = request

    @staticmethod
    def get_model_type() -> type[DataModel]:
        return DataResource.DataModel

class MethodResource(DataResource):
    class MethodModel(BaseModel):
        method: str

        def __init__(self, *, method: str):
            super().__init__(method=method)
            self.method = method

    def __init__(self, method: MethodModel):
        super().__init__(method)
        self.method = method

    @staticmethod
    def get_model_type() -> type[MethodModel]:
        return MethodResource.MethodModel

class FindMethodTask(Task[DataResource, MethodResource]):
    def _do_work(self, input_resource: DataResource) -> MethodResource:
        request = input_resource.request

        method = f""
        instructions = self._generate_cooking_instructions(input_resource.request.recipe_name, ingredient_list)
        return MethodResource(MethodResource.MethodModel(instructions=instructions))

    def __init__(self):
        super().__init__(
            "FindMethodTask",
            "A task that generates a recipe method based on a given recipe name, its ingredients and quantity of each ingredient.",
            DataResource.DataModel,
            MethodResource.MethodModel,
            self._do_work,
        )
