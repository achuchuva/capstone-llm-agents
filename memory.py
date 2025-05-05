from autogen import AssistantAgent, UserProxyAgent, LLMConfig
from autogen import register_function
import sqlite3
#https://www.geeksforgeeks.org/python-sqlite/

print("hello world")

#####short/session memory#####
connection_obj = sqlite3.connect('short_memory.db')

# cursor object
cursor_obj = connection_obj.cursor()

# Drop the SMEMORY ("short memeory") table if already exists.
cursor_obj.execute("DROP TABLE IF EXISTS SMEMORY")

# Creating table
table = """ CREATE TABLE SMEMORY (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Title VARCHAR(255) NOT NULL,
            Date VARCHAR(255) NOT NULL,
            Content VARCHAR(255) NOT NULL
        ); """

cursor_obj.execute(table)

#print("Short term memory is Ready")

# Close the connection
connection_obj.close()

#####Long term memory#####
connection_obj = sqlite3.connect('long_memory.db')

# cursor object
cursor_obj = connection_obj.cursor()

#cursor_obj.execute("DROP TABLE IF EXISTS LMEMORY")#Uncomment when you need to wipe the table
# Creating table
table = """ CREATE TABLE IF NOT EXISTS LMEMORY (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Title VARCHAR(255) NOT NULL,
            Date VARCHAR(255) NOT NULL,
            Content VARCHAR(255) NOT NULL
        ); """

cursor_obj.execute(table)
#cursor_obj.execute('''INSERT INTO LMEMORY (Title, Date, Content) VALUES ('Time to pakenham', '13-04-2025', 'It takes 32 minutes to get to pakenham')''')#Uncomment when you need to add default data

print("Data Inserted in the table: ")
data=cursor_obj.execute('''SELECT * FROM LMEMORY''')
for row in data:
    print(row)
connection_obj.commit()
#print("Long term Memory is Ready")

# Close the connection
connection_obj.close()



#####Model, Agent and functions#####
llm_config = {
    "model": "llama3.2",
    "api_type": "ollama",
    "temperature": 0.5,
}

assistant_agent = AssistantAgent(
    name="Memory Assitant",
    llm_config=llm_config,
    system_message="You are to answer any questions you recive without the use of functions. Only use functions if your absolutely sure they are needed.",
)

user_proxy = UserProxyAgent(
    "user_proxy", code_execution_config={"work_dir": "coding", "use_docker": False}
)

def time_calculation(location_input: str):
    location_time = "The time for " + str(location_input) + " is 12:00 PM"
    return location_time

def most_popular_transport(location_input: str):
    location_transport = "The most popular transport for " + str(location_input) + " is cars"
    return location_transport


register_function(
    time_calculation,
    caller=assistant_agent,
    executor=user_proxy,
    name="time_calculation",  # By default, the function name is used as the tool name.
    description="A function which calculates the time of a location",  # A description of the tool.
)

register_function(
    most_popular_transport,
    caller=assistant_agent,
    executor=user_proxy,
    name="most_popular_transport",  # By default, the function name is used as the tool name.
    description="A function which calculates the most popular transport mode for a location",  # A description of the tool.
)

message = "What is the time for pakenham?."
message2 = "What is the best meal?"
message3 = "What is the most popular transport for melbourne?"

user_proxy.initiate_chat(
    assistant_agent,
    message=message2,
    max_turns=2
)
