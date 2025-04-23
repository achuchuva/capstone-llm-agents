from app import App
from mas.ag2.ag2_agent import AG2MASAgent


trip_activity_agent = AG2MASAgent(
    name="TripActivityAgent",
    description="Get the activities to do on a trip.",
    llm_config=App().config_manager.get_llm_config(use_tools=False),
)
