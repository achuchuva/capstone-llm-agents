"""Entry point of the program."""

import datetime
from agent.knowledge_base_agent import KnowledgeBaseAgent
from app import App
from examples.train_agent import TrainTimetable, TrainTimetables

# from mas.examples.mas_testing import test_basic_mas


def main():
    """Entry point of the program."""
    app = App()
    app.run()

    # test_basic_mas(app)

    def get_knowledge_base_string() -> str:
        """
        Get the knowledge base in string format.

        Returns:
            str: The knowledge base as a string.
        """
        if isinstance(knowledge_base, dict):
            return "\n".join(
                [f"{key}: {value}" for key, value in knowledge_base.items()]
            )
        return str(knowledge_base)

    # create a knowledge base with train timetables
    knowledge_base = TrainTimetables(
        train_timetables=[
            TrainTimetable(
                train_line="Hurstbridge",
                train_time=datetime.datetime(2025, 4, 28, 8, 59).strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                train_destination="Flinders Street",
            ),
            TrainTimetable(
                train_line="Hurstbridge",
                train_time=datetime.datetime(2025, 4, 28, 9, 15).strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                train_destination="Flinders Street",
            ),
            TrainTimetable(
                train_line="Hurstbridge",
                train_time=datetime.datetime(2025, 4, 28, 9, 32).strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                train_destination="Flinders Street",
            ),
            TrainTimetable(
                train_line="Hurstbridge",
                train_time=datetime.datetime(2025, 4, 28, 9, 52).strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                train_destination="Flinders Street",
            ),
            TrainTimetable(
                train_line="Hurstbridge",
                train_time=datetime.datetime(2025, 4, 28, 10, 12).strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                train_destination="Flinders Street",
            ),
            TrainTimetable(
                train_line="Pakenham",
                train_time=datetime.datetime(2025, 4, 28, 8, 56).strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                train_destination="Flinders Street",
            ),
            TrainTimetable(
                train_line="Pakenham",
                train_time=datetime.datetime(2025, 4, 28, 9, 1).strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                train_destination="Flinders Street",
            ),
            TrainTimetable(
                train_line="Pakenham",
                train_time=datetime.datetime(2025, 4, 28, 9, 6).strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                train_destination="Flinders Street",
            ),
        ]
    )

    print("Knowledge base:")
    print(get_knowledge_base_string())
    print("\n\n")
    # Load in knowledge base agent
    agent = KnowledgeBaseAgent(
        name="TrainAgent",
        system_message=(
            f"""You are a train timetable assistant. You can answer questions about train timetables.
            Answer ONLY using the following knowledge base:\n\n
            {get_knowledge_base_string()}\n\n"
            If you do not know the answer based on the knowledge base, say 'I'm sorry, I don't have information on that.'
            """
        ),
        llm_config=app.config_manager.get_llm_config(use_tools=False),
        knowledge_base=knowledge_base,
    )

    query = {
        "role": "user",
        "content": "It is 9am. What time is the next train to Flinders Street on the Pakenham Line?",
    }

    response = agent.generate_reply(messages=[query])
    print(response["content"])


if __name__ == "__main__":
    main()
