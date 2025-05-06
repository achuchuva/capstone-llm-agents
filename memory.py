from autogen import AssistantAgent, UserProxyAgent, register_function
import sqlite3

SHORT_MEMORY_DB = "short_memory.db"
LONG_MEMORY_DB = "long_memory.db"


def setup_short_memory():
    conn = sqlite3.connect(SHORT_MEMORY_DB)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS SMEMORY")
    cursor.execute(
        """
        CREATE TABLE SMEMORY (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Title TEXT NOT NULL,
            Date TEXT NOT NULL,
            Content TEXT NOT NULL
        );
    """
    )
    conn.close()


def setup_long_memory():
    conn = sqlite3.connect(LONG_MEMORY_DB)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS LMEMORY (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Title TEXT NOT NULL,
            Date TEXT NOT NULL,
            Content TEXT NOT NULL
        );
    """
    )
    print("Long-term memory contents:")
    for row in cursor.execute("SELECT * FROM LMEMORY"):
        print(row)
    conn.commit()
    conn.close()


def save_to_long_memory(Title: str, Date: str, Content: str) -> str:
    try:
        conn = sqlite3.connect(LONG_MEMORY_DB)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO LMEMORY (Title, Date, Content) VALUES (?, ?, ?)",
            (Title, Date, Content),
        )
        conn.commit()
        return f"Content saved to memory as --> (Title: {Title} Date: {Date} Content: {Content})"
    except Exception as e:
        return f"An error occurred while saving: {e}"
    finally:
        conn.close()


def get_all_memory_titles() -> str:

    conn = sqlite3.connect(LONG_MEMORY_DB)
    cursor = conn.cursor()
    cursor.execute("SELECT ID, Title FROM LMEMORY")
    results = cursor.fetchall()
    conn.close()

    if results:
        return "\n".join([f"ID: {row[0]}, Title: {row[1]}" for row in results])
    else:
        return "No content found in long-term memory."


def load_memory_by_index(selection_index: int):
    conn = sqlite3.connect(LONG_MEMORY_DB)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT ID, Title, Date, Content FROM LMEMORY
        WHERE ID = ?
        """,
        (selection_index,),
    )
    result = cursor.fetchone()
    conn.close()
    if result:
        return f"ID: {result[0]}, Title: {result[1]}, Date: {result[2]}, Content: {result[3]}"
    else:
        return "No content found for the given ID."


# random stuff
def time_calculation(location_input: str) -> str:
    return f"The time for {location_input} is 12:00 PM"


def most_popular_transport(location_input: str) -> str:
    return f"The most popular transport for {location_input} is cars"


llm_config = {
    "model": "llama3.2",
    "api_type": "ollama",
    "temperature": 0.5,
}

assistant_agent = AssistantAgent(
    name="MemoryAssistant",
    llm_config=llm_config,
    system_message="You are to answer any questions to the best of your knowledge. Only save results to your long memory when you know the answer is correct.",
)

user_proxy = UserProxyAgent(
    "user_proxy", code_execution_config={"work_dir": "coding", "use_docker": False}
)

# funcs
register_function(
    time_calculation,
    caller=assistant_agent,
    executor=user_proxy,
    name="time_calculation",
    description="Calculate the current time for a given location.",
)

register_function(
    most_popular_transport,
    caller=assistant_agent,
    executor=user_proxy,
    name="most_popular_transport",
    description="Determine the most popular mode of transport for a location.",
)

register_function(
    save_to_long_memory,
    caller=assistant_agent,
    executor=user_proxy,
    name="save_to_long_memory",
    description="Save valid results to the long-term memory database.",
)

register_function(
    get_all_memory_titles,
    caller=assistant_agent,
    executor=user_proxy,
    name="Load_memory",
    description="Load all memory titles from the long-term memory database.",
)

register_function(
    load_memory_by_index,
    caller=assistant_agent,
    executor=user_proxy,
    name="Load_memory_by_index",
    description="Load memory by index from the long-term memory database.",
)


if __name__ == "__main__":
    print("Initializing memory databases...")
    setup_short_memory()
    # setup_long_memory()

    user_proxy.initiate_chat(
        assistant_agent,
        message="Prompt the assistant agent to be prepared for further questions.",
        max_turns=10,
    )
