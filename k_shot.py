import ollama


MODEL = "gemma3"


class Message:
    """Message class."""

    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content

    def to_dict(self) -> dict:
        return {"role": self.role, "content": self.content}

    def __str__(self):
        return f"{self.role}: {self.content}"


class UserMessage(Message):
    """User message class."""

    def __init__(self, content: str):
        super().__init__("user", content)


class AssistantMessage(Message):
    """Assistant message class."""

    def __init__(self, content: str):
        super().__init__("assistant", content)


class Example:
    """Example class for k-shot prompting."""

    def __init__(self, user_message: UserMessage, assistant_message: AssistantMessage):
        self.user_message = user_message
        self.assistant_message = assistant_message


def k_shot(examples: list[Example], user_message: UserMessage) -> str:
    """
    Get a response from the model using k-shot learning.
    """
    messages = []

    for example in examples:
        messages.append(example.user_message.to_dict())
        messages.append(example.assistant_message.to_dict())

    messages.append(user_message.to_dict())

    # input
    print("Input:")
    # pretty print the input
    for message in messages:
        print(message)

    response = ollama.chat(
        model=MODEL,
        messages=messages,
    )

    return response["message"]["content"]


# without k shot
print("\nWithout k shot:")

user_message = UserMessage(
    "Email: 'Book a table for two at 7pm on Friday. Give a single line command as a function with named parameters.'\nCommand: "
)

response = ollama.chat(
    model=MODEL,
    messages=[
        user_message.to_dict(),
    ],
)

print("Input:")
# pretty print the input
print(user_message.to_dict())

print("Response:")
print(response["message"]["content"])

# with k shot

print("With k shot:")

examples = [
    Example(
        UserMessage(
            "Email: 'Can you schedule a meeting for Thursday at 3pm with Bob?'\nCommand: "
        ),
        AssistantMessage("schedule_meeting(time='Thursday 3pm', person='Bob')"),
    ),
    Example(
        UserMessage("Email: 'Remind me to call Alice tomorrow morning.'\nCommand:"),
        AssistantMessage("set_reminder(time='tomorrow morning', task='call Alice')"),
    ),
]

user_message = UserMessage("Email: 'Book a table for two at 7pm on Friday.'\nCommand:")

response = k_shot(examples, user_message)
print("Response:")
print(response)
