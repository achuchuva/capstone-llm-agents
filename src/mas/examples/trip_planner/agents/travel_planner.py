from app import App
from mas.ag2.ag2_agent import AG2MASAgent


travel_planner_agent = AG2MASAgent(
    name="TravelPlannerAgent",
    description="Plan a journey between two places (e.g. train stations or tram stops)",
    llm_config=App().config_manager.get_llm_config(use_tools=False),
)
