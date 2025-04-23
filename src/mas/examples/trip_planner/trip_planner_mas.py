"""MAS for planning trips"""

from app import App
from mas.ag2.ag2_task import AG2Task
from mas.examples.trip_planner.resources.activity import ActivityResource
from mas.examples.trip_planner.resources.travel import TravelResource
from mas.examples.trip_planner.resources.travel_plan import TravelPlanResource
from mas.examples.trip_planner.resources.trip_activities import ActivitiesResource
from mas.examples.trip_planner.resources.trip_idea import TripIdeaResource
from mas.examples.trip_planner.resources.weather import WeatherResource
from mas.multi_agent_system import MultiAgentSystem
from mas.resource_alias import ResourceAlias
from mas.resources.empty import EmptyResource
from mas.task import Task

from utils.string_template import generate_str_using_template

from mas.examples.trip_planner.agents.weather_agent import better_weather_agent
from mas.examples.trip_planner.agents.trip_activity import trip_activity_agent
from mas.examples.trip_planner.tasks.weather_task import do_weather_task


class TripPlannerMAS(MultiAgentSystem):
    """Trip Planner MAS"""

    descriptor_mapping: dict[str, Task]

    def __init__(self, app: App):
        """
        Initialise the Trip Planner MAS.
        """

        # resource aliases
        alias = ResourceAlias()

        # add the resources
        alias.add_resource_alias("empty", EmptyResource)
        alias.add_resource_alias("trip_idea", TripIdeaResource)
        alias.add_resource_alias("trip_activities", ActivitiesResource)
        alias.add_resource_alias("travel_plan", TravelPlanResource)
        alias.add_resource_alias("travel", TravelResource)
        alias.add_resource_alias("weather", WeatherResource)
        alias.add_resource_alias("activity", ActivityResource)

        # add the tasks
        tasks: list[Task] = []

        # TravelIdeaResource -> WeatherResource
        get_weather_at_place_and_time = Task(
            name="GetWeatherAtPlaceAndTime",
            description="Get the weather at a place and time.",
            input_resource=TripIdeaResource,
            output_resource=WeatherResource,
            do_work=do_weather_task,
        )
        # TripIdeaResource -> ActivitiesResource
        generate_trip_activity_ideas = AG2Task(
            name="GenerateTripActivityIdeas",
            description="Generate trip activity ideas.",
            input_resource=TripIdeaResource,
            output_resource=ActivitiesResource,
            generate_str=generate_str_using_template(
                "I want to know {number_of_activities} activities I can do in {city}. Make sure the duration is at most 120 minutes.",
            ),
            agent=trip_activity_agent,
        )
        # ActivitiesResource -> TravelPlanResource
        create_travel_plan_between_activities = AG2Task(
            name="CreateTravelPlanBetweenActivities",
            description="Create a travel plan between activities.",
            input_resource=ActivitiesResource,
            output_resource=TravelPlanResource,
            generate_str=generate_str_using_template(
                "I want to know the travel plan between the following activities. The start and end locations should be train stations or tram stops near to the activities. Include train station/tram stop in the name, and make they are real train station/ tram stops. Make sure the duration is not longer than 20 minutes for each travel: {activities}.",
            ),
            agent=trip_activity_agent,
        )

        for task in tasks:
            self.add_task(task)

        super().__init__(alias)

        # set descriptor mapping
        self.descriptor_mapping = {
            "at_place_and_time": get_weather_at_place_and_time,
            "trip_in_city": generate_trip_activity_ideas,
            "with_activities": create_travel_plan_between_activities,
        }
