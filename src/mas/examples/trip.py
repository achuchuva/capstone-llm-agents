"""Test file for basic MAS"""

from app import App

from mas.examples.trip_planner.trip_planner_mas import TripPlannerMAS
from mas.query.mas_query import MASQuery


def trip_app(app: App):
    """Test trip planner MAS."""

    mas = TripPlannerMAS(app)

    yaml_file = "./resource/example/trip.yaml"

    mas_query = MASQuery.from_yaml(yaml_file)

    output_resources = mas.solve_query(mas_query, mas.descriptor_mapping)

    # print the output resources
    print("Output:")
    for output_resource in output_resources:
        print(output_resource.model.model_dump_json(indent=4, exclude_unset=True))
