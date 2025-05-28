import tkinter as tk
import time  # for delay
import threading
import pyglet  # for custom font stuff
from tkinter import filedialog, messagebox
from capabilities.knowledge_base import Document
from core.app_api import AppAPI

import os


class UserInterface:
    """A simple CLI interface for interacting with MASAPI."""

    def __init__(self, api: AppAPI):
        self.api = api
        # tkinter window
        self.root = tk.Tk()
        self.root.title("MAS GUI")
        self.root.geometry("800x500")
        self.custom_font = self.load_custom_font(
            "user_interface/fonts/NebulaSans-Medium.ttf", size=16
        )  # just edit if you want a diff font, not certain this is working though
        self.setup_layout()
        self.create_buttons()
        # flag for the window type, whether it's actively in the messaging/chat mode
        self.messaging_mode = False

    def load_custom_font(self, font_path, size):
        try:
            pyglet.font.add_file(font_path)
            font_name = font_path.split("/")[-1].replace(".ttf", "")
            return (font_name, size)
        except Exception as e:
            print(f"Error loading font: {e}")
            return ("Helvetica", size)

    # main window formatting
    def setup_layout(self):
        # main window frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # side buttons frame
        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        # output window frame
        self.output_frame = tk.Frame(self.main_frame)
        self.output_frame.pack(
            side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10
        )

        # text box output frame
        self.text_output = tk.Text(
            self.output_frame,
            height=20,
            wrap=tk.WORD,
            font=(self.custom_font[0], self.custom_font[1]),
        )
        self.text_output.pack(fill=tk.BOTH, expand=True)
        self.text_output.config(state=tk.DISABLED)

        # input frame (below the main output box)
        self.text_input = tk.Entry(
            self.output_frame, font=(self.custom_font[0], self.custom_font[1])
        )
        self.text_input.pack(fill=tk.X, padx=10, pady=5)
        self.text_input.bind("<Return>", self.submit_query)

    def create_buttons(self):
        buttons = [
            ("List Agents", self.list_agents),
            ("View Chat/Query MAS", self.enter_messaging_mode),
            ("Add Document", self.add_document),
            ("List Documents", self.list_documents),
            ("Exit", self.root.quit),
        ]
        for label, command in buttons:
            button = tk.Button(
                self.button_frame,
                text=label,
                width=20,
                command=command,
                font=(self.custom_font[0], self.custom_font[1]),
            )
            button.pack(pady=5)

    def run(self):
        """Run the CLI interface."""

        # self.clear_screen()

        print("Welcome to the MAS CLI!")
        while True:

            print("\nMenu:")
            print("1. List Agents")
            print("2. Query MAS")
            print("3. View Chat History")
            print("4. Add Document to Agent")
            print("5. List Documents")
            print("6. Exit\n")
            choice = input("Enter your choice: ").strip()

            self.clear_screen()

            if choice == "1":
                self.list_agents()
            elif choice == "2":
                self.query_mas()
            elif choice == "3":
                self.view_chat_history()
            elif choice == "4":
                self.add_document()
            elif choice == "5":
                self.list_documents()
            elif choice == "6":
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

    def query_mas(self):
        """Query the MAS with a prompt."""
        query = input("Enter your query: ")
        response = self.api.mas_api.query_mas(query)
        print("Response:")
        print(response)

    def view_chat_history(self):
        """View the chat history."""
        history = self.api.mas_api.get_chat_history()

        # length check
        if len(history.messages) == 0:
            print("No chat history available.")
            return

        self.text_input.delete(0, tk.END)
        self.clear_output()
        self.start_messaging_mode()

        # loading window while waiting for output
        loading_popup = tk.Toplevel(self.root)
        loading_popup.title("Loading...")
        loading_popup.geometry("200x100")
        tk.Label(
            loading_popup,
            text="Loading...",
            font=(self.custom_font[0], self.custom_font[1]),
        ).pack(expand=True)
        loading_popup.transient(self.root)
        loading_popup.grab_set()

        # thread to receive response upon sending query, bit redundant/should make more funcs so less overlap with initial grab
        def query_thread():
            try:
                self.api.query_mas(query)
                time.sleep(1.5)  # Wait for response
                history = self.api.get_chat_history()

                if history and history.messages:
                    result = "Chat History:\n" + "\n".join(
                        f"- {msg.who}: {msg.content}" for msg in history.messages
                    )
                else:
                    result = "Sorry, I couldn't find a response."
                self.root.after(0, lambda: self.print_output(result))

            except Exception as e:
                self.root.after(0, lambda: self.print_output(f"An error occurred: {e}"))
            # kill popup
            finally:
                self.root.after(0, loading_popup.destroy)
                self.root.after(0, self.end_messaging_mode)

        threading.Thread(target=query_thread, daemon=True).start()

    # just flag stuff
    def start_messaging_mode(self):
        self.messaging_mode = True

    def end_messaging_mode(self):
        self.messaging_mode = False

    # add doc button
    def add_document(self):
        """Add a document to an agent."""
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
        """List all documents in the MAS."""
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
        self.api.exit()
        print("Exiting the MAS CLI. Goodbye!")
