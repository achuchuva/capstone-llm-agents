from app import App
from mas.ag2.ag2_agent import AG2MASAgent


better_weather_agent = AG2MASAgent(
    name="BetterWeatherAgent",
    description="Get the weather at a place and time.",
    llm_config=App().config_manager.get_llm_config(use_tools=False),
)
