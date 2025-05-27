import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout, QGridLayout, QLabel, QLineEdit
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import pyqtSlot

class App(QDialog):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 layout - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 500
        self.height = 500
        self.chat_output_one = QLabel()
        self.chat_output_one.setStyleSheet("background-color: blue; font-size: 18px; margin-right: 80px;")
        self.chat_output_two = QLabel()
        self.chat_output_two.setStyleSheet("background-color: red;")

        # Create a QLineEdit for typing new messages
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Type your message here...and press Enter key.")
        self.message_input.returnPressed.connect(self.send_message)

        layout = QVBoxLayout()

        layout.addWidget(self.message_input)

        # Set the layout for the central widget
        #central_widget.setLayout(layout)

        # Initialize chat history
        self.chat_history = []
        self.initUI()

    def send_message(self):
        # Get the message from the input field
        message = self.message_input.text()

        # Append the message to the chat history
        self.chat_history.append(message)

        # Update the chat display
        self.update_chat_display()

        # Clear the input field
        self.message_input.clear()

    def update_chat_display(self):
        # Display the chat history in the QLabel
        chat_text = "\n".join(self.chat_history)
        self.chat_output_one.setText(chat_text)

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createGridLayout()

        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        windowLayout.addWidget(self.message_input)#used to add the text intput
        self.setLayout(windowLayout)

        self.show()

    def createGridLayout(self):
        self.horizontalGroupBox = QGroupBox("Box 1")
        #self.horizontalGroupBox.setStyleSheet("QGroupBox { border: none; }")
        layout = QGridLayout()

        #layout.setColumnStretch(1, 4)
        #layout.setColumnStretch(2, 4)

        #chat_output_one = QLabel()
        #chat_output_two = QLabel()

        self.chat_output_one.setText("Chat output 1")
        self.chat_output_two.setText("Chat output 2")

        layout.addWidget(self.chat_output_one,0,0)
        layout.addWidget(self.chat_output_two,0,1)

        self.horizontalGroupBox.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec())
