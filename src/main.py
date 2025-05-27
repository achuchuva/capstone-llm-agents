from autogen import ConversableAgent
from app import App
from core.capability import Capability
from implementations.faiss_kb import FAISSKnowledgeBase


default_capabilities: list[Capability] = []
app = App(default_capabilities)

# Capabilities
# ============

# add kb
default_capabilities.append(
    FAISSKnowledgeBase(
        ["pdf", "txt", "docx"],
        1000,
        3,
        # ["sprint", "retrospective", "scrum", "burndown", "velocity"],
        # (
        #     "This document is related to agile sprint reports and can mention retrospectives, user stories, velocity charts, and burndown trends."
        # ),
    )
)

# Agents
# ======

# add agent
app.add_ag2_agent(
    ConversableAgent(
        name="Assistant",
        system_message="You are a helpful assistant.",
        llm_config={"api_type": "ollama", "model": "gemma3"},
    ),
    default_capabilities,
)

# add specialised agent
# app.add_ag2_agent(
#     ConversableAgent(
#         name="Sprint Report Assistant",
#         system_message="""
#             You are an assistant that specialises in analysing agile sprint reports and will only answer sprint related queries.
#             Disregard any other queries politely and inform the user that you can only answer sprint related queries.
#         """,
#         llm_config={"api_type": "ollama", "model": "gemma3"},
#     ),
#     default_capabilities,
# )

app.run()
