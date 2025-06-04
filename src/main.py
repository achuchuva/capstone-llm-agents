# NOTE: For now just do what you need to make it work but I will fix it later
from autogen import ConversableAgent

from dotenv import load_dotenv

from app import App

from implementations.memory import Memory
from implementations.faiss_kb import FAISSKnowledgeBase
from implementations.communication_interface import SimpleCommunicationInterface
from implementations.ag2_tools import CurrentDateTimeTool, WeekdayTool, MathTool
from implementations.ag2_tools_manager import AG2ToolsManager

load_dotenv()


app = App()

# Capabilities
# ============

# kb
app.add_capability(FAISSKnowledgeBase(["pdf", "txt"], 1000, 3))


simple_comms = SimpleCommunicationInterface()
# communication interface
app.add_capability(simple_comms)

# add tools manager
defaults_tools = AG2ToolsManager(app)

calendar_tools = AG2ToolsManager(app)
calendar_tools.add_tool(CurrentDateTimeTool())
calendar_tools.add_tool(WeekdayTool())

math_tools = AG2ToolsManager(app)
math_tools.add_tool(MathTool())


app.add_capability(defaults_tools)

# memory
# app.add_capability(Memory())

# Agents
# ======

# add agent
app.add_ag2_agent(
    ConversableAgent(
        name="Assistant",
        system_message="You are a helpful assistant.",
        llm_config=app.config.get_llm_config(),
    ),
)

# math agent
app.add_ag2_agent(
    ConversableAgent(
        name="Math Agent",
        system_message="You are a math expert. You can solve mathematical problems and perform calculations.",
        llm_config=app.config.get_llm_config(),
    ),
    [math_tools, simple_comms],
)

# writer agent
app.add_ag2_agent(
    ConversableAgent(
        name="Writer Agent",
        system_message="You are a creative writer.",
        llm_config=app.config.get_llm_config(),
    ),
)

# calendar agent
app.add_ag2_agent(
    ConversableAgent(
        name="Calendar Agent",
        system_message="You are a calendar management expert. You know about the current date and time, and can help with scheduling.",
        llm_config=app.config.get_llm_config(),
    ),
    [calendar_tools, simple_comms],
)

# research agent
app.add_ag2_agent(
    ConversableAgent(
        name="Research Agent",
        system_message="You are a research expert. You can research and summarise documents.",
        llm_config=app.config.get_llm_config(),
    ),
)


app.run()
