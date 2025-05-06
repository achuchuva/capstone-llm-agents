from app import App
from examples.sql_query_agent import SQLQueryAgent
from examples.database_agent import DatabaseAgent
from knowledge_base.database_model import clean_sql_string, run_database_query
from knowledge_base.database_schema_model import get_database_schema


def run_database_kb(app: App):
    """
    Run the example.
    This example demonstrates how to use an SQL database as a knowledge base for a simple customer data agent.
    """
    database_schema_kb = get_database_schema()

    database_agent = DatabaseAgent(
        name="Database Agent",
        llm_config=app.config_manager.get_llm_config(use_tools=False),
        knowledge_base=database_schema_kb,
    )

    print(f"Database Schema Knowledge Base:\n{database_schema_kb}")

    query = {
        "role": "user",
        "content": "What is the name of the customer with CustomerId 1?",
    }

    response = database_agent.generate_reply(messages=[query])
    print(response["content"])

    sql_query = clean_sql_string(response["content"])
    sql_query_kb = run_database_query(query=sql_query)

    print(f"SQL Query: {sql_query_kb}")

    sql_query_agent = SQLQueryAgent(
        name="SQL Query Agent",
        llm_config=app.config_manager.get_llm_config(use_tools=False),
        knowledge_base=sql_query_kb,
    )

    response = sql_query_agent.generate_reply(messages=[query])
    print(response["content"])
