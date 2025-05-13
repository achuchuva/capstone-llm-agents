import autogen
import os
#https://github.com/Andyinater/AutoGen_MemoryManager
# Where the memory path will be located.
mem_path = "MemFile.txt"


llm_config = {
    "model": "llama3.2",
    "api_type": "ollama",
    "temperature": 0.5,
}


def rewrite_memory(memory):
    if not os.path.exists(mem_path):
        with open(mem_path, 'w') as f:
            f.write(memory + '|')

    else:
        with open(mem_path, 'w') as f:
            f.write(memory + '|')

    return True

def read_from_memory():
    if os.path.exists(mem_path):
        with open(mem_path, 'r') as f:
            d = f.read()
    else:
        d = "NO LONG TERM MEMORY FOUND"
    return d

def write_to_memory_intent(message):
    user_proxy_for_functions.initiate_chat(
    mem_manager,
    message=message,
)

def read_from_memory_intent():
    if os.path.exists(mem_path):
        with open(mem_path, 'r') as f:
            d = f.read()
    else:
        d = "NO LONG TERM MEMORY FOUND"
    return d


# create the MemoryManagerAgent
mem_manager = autogen.AssistantAgent(
    name="mem_manager",
    llm_config=llm_config,
    system_message = """You are a helpful AI assistant acting as a memory manager. You will be asked to either write a message to memory, or to read the memory.
    If you are being asked to write to memory, you should:
        1. Read the existing memory: Before you decide if a memory should be added, you need to know what memories already exist.
        2. If you deem the message to be new information that is not represented in the existing memories, you should rewrite the existing memories such that the information is now incorporated.

    The memory is formatted as a series of statements seperated by the '|' character.

    For example, the existing memory might look like this:
        "User is allergic to seafood| User likes dogs| User is from Canada"

    In this example, if you were requested to write a message to memory that was "User likes cats", when you go to rewrite the memory, it should look like this:
        "User is allergic to seafood| User likes dogs, cats| User is from Canada"


    Sometimes it might be best to remove content from the memory. For example, if the existing memory looked like this:
        "User is allergic to seafood| User likes dogs, cats| User is from Canada"

    And you were asked to write a message to memory that was "User does not like dogs", when you go to rewrite the memory, it should look like this:
        "User is allergic to seafood| User likes cats| User is from Canada"

    The changes to the rewritten memory can span multiple statements, if appropriate. The point is to keep the entire memory as accurate and representative as possible.

    Do not participate in any form of conversation.

    After you have finished your task, respond with "TERMINATE"
""",
)







# create the ConversingAgent
conversing_agent = autogen.AssistantAgent(
    name="assistant",
    llm_config=llm_config,
    system_message = "You are a helpful AI assistant, with even more helpful tools. Use one or more tools BEFORE talking to the user. Converse with the user to help them achieve their goals, but use tools too. write things to memory often. read from memory before asking the user. It is critically important that, whenever the user gives details about themselves or their preferences, you write it to memory. If this is the start of a new conversation, the very first thing you must do is read your memory. If no long term memory is found, you should start by asking who you're talking to.",
)

# create the UserProxyAgent used by the human to converse
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="ALWAYS",
    max_consecutive_auto_reply=10,
    code_execution_config={"work_dir": "_test", "use_docker": False},#maybe a docker shoudld be needed?
    function_map={"write_to_memory_intent": write_to_memory_intent, "read_from_memory_intent": read_from_memory_intent, "rewrite_memory": rewrite_memory, "read_from_memory": read_from_memory},
)

# create the UserProxyAgent_ForFunctions to be used by the MemoryManager to execute function calls in chat
user_proxy_for_functions = autogen.UserProxyAgent(
    name="user_proxy_for_functions",
    human_input_mode="TERMINATE",
    max_consecutive_auto_reply=10,
    code_execution_config={"work_dir": "_test", "use_docker": False},
    function_map={"write_to_memory_intent": write_to_memory_intent, "read_from_memory_intent": read_from_memory_intent, "rewrite_memory": rewrite_memory, "read_from_memory": read_from_memory},
)

# the assistant receives a message from the user, which contains the task description
user_proxy.initiate_chat(
    conversing_agent,
    message="""(User is present)""",
)
