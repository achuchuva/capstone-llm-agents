from app import App
from examples.train_timetable_agent import TrainTimetableAgent
from knowledge_base.data_model import train_timetables


def run_base_model_kb(app: App):
    """
    Run the example.
    This example demonstrates how to use pydantic's BaseModel as knowledge base for a simple train timetable agent.
    """
    train_timetable_agent = TrainTimetableAgent(
        name="Train Timetable Agent",
        llm_config=app.config_manager.get_llm_config(use_tools=False),
        knowledge_base=train_timetables.model_dump_json(indent=2),
    )

    train_timetable_query = {
        "role": "user",
        "content": "It is 9:00am, 28th of April. What time is the next train to Flinders Street on the Hurstbridge Line?",
    }

    response = train_timetable_agent.generate_reply(messages=[train_timetable_query])
    print(response["content"])
