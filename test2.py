import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout, QGridLayout, QLabel, QLineEdit, QScrollBar, QScrollArea
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtCore import Qt

class App(QDialog):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 layout - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 700
        self.height = 500


        self.chat_output_one = QLabel()
        self.chat_output_two = QLabel()
        #self.chat_output_two.setStyleSheet("background-color: red;")

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
        self.chat_output_two.setText(chat_text)

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
        self.horizontalGroupBox = QGroupBox()
        self.horizontalGroupBox.setStyleSheet("QGroupBox {border: none;}")
        #self.horizontalGroupBox.setStyleSheet("border: none;")
        #self.horizontalGroupBox.setStyleSheet('QGroupBox:title {subcontrol-origin: margin; subcontrol-position: top center;}')
        layout = QGridLayout()

        #second boxes to put inside of first box
        groupbox1 = QGroupBox("Reasoning")
        groupbox1.setStyleSheet("QGroupBox {background-color: blue; margin-top: 20px; margin-right: 30px;}  QGroupBox::title {subcontrol-origin: margin; subcontrol-position: top center; margin-right: 30px;}")
        groupbox1_layout = QVBoxLayout()
        groupbox1_layout.addWidget(self.chat_output_one, alignment=Qt.AlignmentFlag.AlignTop)
        groupbox1.setLayout(groupbox1_layout)

        groupbox2 = QGroupBox("Output")
        groupbox2.setStyleSheet("QGroupBox {background-color: red; margin-top: 20px; margin-left: 30px;}  QGroupBox::title {subcontrol-origin: margin; subcontrol-position: top center; margin-left: 30px;}")
        groupbox2_layout = QVBoxLayout()
        groupbox2_layout.addWidget(self.chat_output_two, alignment=Qt.AlignmentFlag.AlignTop)
        groupbox2.setLayout(groupbox2_layout)

        #layout.setColumnStretch(1, 4)
        #layout.setColumnStretch(2, 4)

        #chat_output_one = QLabel()
        #chat_output_two = QLabel()

        self.chat_output_one.setText("Chat output 1")
        self.chat_output_two.setText("Chat output 2")


        layout.addWidget(groupbox1,0,0)
        layout.addWidget(groupbox2, 0, 1)
        #layout.addWidget(scroll_area)

        self.horizontalGroupBox.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec())
