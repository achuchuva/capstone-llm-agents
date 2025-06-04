from capabilities.knowledge_base import Document
import os
from user_interface.user_interface import UserInterface


class CLI(UserInterface):
    """A simple CLI interface for interacting with MASAPI and SpaceAPI."""

    def run(self):
        print("Welcome to the MAS CLI!")
        while True:
            print("\nMenu:")
            print("1. List Agents")
            print("2. List Spaces")
            print("3. Query MAS")
            print("4. View Chat History for Space")
            print("5. Add Document to Agent")
            print("6. List Documents")
            print("7. Exit\n")
            choice = input("Enter your choice: ").strip()
            self.clear_screen()

            if choice == "1":
                self.list_agents()
            elif choice == "2":
                self.list_spaces()
            elif choice == "3":
                self.query_mas()
            elif choice == "4":
                self.view_chat_history()
            elif choice == "5":
                self.add_document()
            elif choice == "6":
                self.list_documents()
            elif choice == "7":
                self.exit()
                break
            else:
                print("Invalid choice. Try again.")

    def list_agents(self):
        """List all agents in the MAS."""
        agents = self.api.mas_api.get_agents()
        if agents:
            print("Agents:")
            for agent in agents:
                print(f"- {agent.name}")
        else:
            print("No agents found.")

    def list_spaces(self):
        """List all spaces in the MAS."""
        spaces = self.api.space_api.get_spaces()
        if spaces:
            print("Spaces:")
            for space in spaces:
                print(f"- {space.name}")
        else:
            print("No spaces found.")

    def query_mas(self):
        """Query the MAS using the original MAS API."""
        query = input("Enter your query: ")
        response = self.api.mas_api.query_mas(query)
        print("Response:")
        print(response)

    def view_chat_history(self):
        """View the chat history for Admin or User space."""
        spaces = self.api.space_api.get_spaces()

        admin_space = next((s for s in spaces if "Main Space" in s.name), None)
        user_space = next((s for s in spaces if "User Space" in s.name), None)

        if not admin_space and not user_space:
            print("No spaces found.")
            return

        print("Select space to view chat history:")
        if admin_space:
            print("1. Admin")
        if user_space:
            print("2. User")

        choice = input("Enter your choice: ").strip()

        if choice == "1" and admin_space:
            space = admin_space
        elif choice == "2" and user_space:
            space = user_space
        else:
            print("Invalid choice or space not available.")
            return

        history = self.api.space_api.get_chat_history_for_space(space)

        if len(history.messages) == 0:
            print("No chat history available.")
            return

        print(f"Chat History for {space.name}:")
        for entry in history.messages:
            print(f" - {entry.who}: {entry.content}")

    def add_document(self):
        """Add a document to an agent using the original MAS API."""
        agent_name = input("Enter agent name: ")
        try:
            agent = self.api.mas_api.get_agent(agent_name)
        except KeyError:
            print(f"No agent found with name: {agent_name}")
            return

        path = input("Enter document path: ")
        extension = path.split(".")[-1]
        document = Document(path=path, extension=extension)
        self.api.mas_api.add_document(document, agent)
        print("Document added successfully.")

    def list_documents(self):
        """List all documents using the original MAS API."""
        docs = self.api.mas_api.get_documents()
        if docs:
            print("Documents:")
            for doc in docs:
                print(f"- {doc.path}")
        else:
            print("No documents available.")

    def clear_screen(self):
        """Clear the console screen."""
        os.system("cls" if os.name == "nt" else "clear")

    def exit(self):
        """Exit the CLI interface."""
        super().exit()
        print("Exiting the MAS CLI. Goodbye!")

    def _get_space_by_name(self, name):
        """Helper to get a space by name."""
        for space in self.api.space_api.get_spaces():
            if space.name == name:
                return space
        return None
