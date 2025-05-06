"""Entry point of the program."""

from app import App
from examples.train_timetable_agent import TrainTimetableAgent
from knowledge_base.data_model import train_timetables

# from mas.examples.mas_testing import test_basic_mas


def main():
    """Entry point of the program."""
    app = App()
    app.run()

    # test_basic_mas(app)
    agent = TrainTimetableAgent(
        name="Train Timetable Agent",
        llm_config=app.config_manager.get_llm_config(use_tools=False),
        knowledge_base=train_timetables.model_dump_json(indent=2),
    )

    query = {
        "role": "user",
        "content": "It is 9:00am, 28th of April. What time is the next train to Flinders Street on the Hurstbridge Line?",
    }

    response = agent.generate_reply(messages=[query])
    print(response["content"])


if __name__ == "__main__":
    main()
