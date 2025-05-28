from core.agent import Agent
from core.capabiliity_manager import AgentCapabilities
from core.chat import ChatHistory
from core.mas import MAS

from capabilities.knowledge_base import Document, Folder


class MASAPI:
    """API layer between the user interface and the MAS."""

    documents: list[Document]
    agent_documents: dict[str, list[Document]]
    folders: list[Folder]

    def __init__(self, mas: MAS):
        self.mas = mas
        self.documents = []
        self.folders = []

        # a dictionary of agent names to documents
        self.agent_documents = {}

    def add_document(self, document: Document, agent: Agent):
        """Add a document to the MAS."""
        ingested = agent.capabilties.knowledge_base.ingest_document(document)
        if ingested:
            self.documents.append(document)
            self.agent_documents.setdefault(agent.name, []).append(document)

    def add_folder(self, folder: Folder, agent: Agent):
        """Add a folder of documents to the MAS."""
        ingested_docs = agent.capabilties.knowledge_base.ingest_folder(folder)
        for document in ingested_docs:
            self.documents.append(document)
            self.agent_documents.setdefault(agent.name, []).append(document)

        self.folders.append(folder)

    def query_mas(self, query: str) -> str:
        """Query the MAS with a prompt."""
        return self.mas.handle_prompt_from_user(query)

    def get_agents(self) -> list[Agent]:
        """Get a list of agents in the MAS."""
        return self.mas.get_agents()

    def get_agent_capabilities(self, agent: Agent) -> AgentCapabilities:
        """Get the capabilities of an agent."""
        return agent.get_capabilities()

    def get_agent(self, name: str) -> Agent:
        """Get an agent by name."""
        return self.mas.get_agent(name)

    def get_documents(self) -> list[Document]:
        """Get a list of documents in the MAS."""
        return self.documents

    def get_agent_documents(self, agent: Agent) -> list[Document]:
        """Get a list of documents for an agent."""
        return self.agent_documents.get(agent.name, [])

    def get_chat_history(self) -> ChatHistory:
        """Get the chat history."""
        return self.mas.chat_history

    def get_folders(self) -> list[Folder]:
        """Get a list of folders in the MAS."""
        return self.folders

    def update_folder(self, folder: Folder, agent: Agent):
        """Update a folder of documents in the MAS."""
        kb = agent.capabilties.knowledge_base

        deleted_docs = kb.update_folder(folder)

        deleted_doc_paths = [doc.path for doc in deleted_docs]

        # get matching documents in the agent's document list
        matching_docs = [doc for doc in self.documents if doc.path in deleted_doc_paths]

        # Remove deleted documents from the agent's document list
        for doc in matching_docs:
            if doc in self.documents:
                self.documents.remove(doc)
            if doc in self.agent_documents.get(agent.name, []):
                self.agent_documents[agent.name].remove(doc)
