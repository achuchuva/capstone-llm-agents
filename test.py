import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QLabel,
    QStackedLayout,
    QFileDialog,
    QScrollBar,
    QScrollArea,
    QFrame,
    QGroupBox,
    QGridLayout,
)
from PyQt6.QtGui import (
    QIcon,
    QFont
)
from PyQt6.QtCore import Qt
from qt_material import apply_stylesheet

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MAS Application")

        central = QWidget()
        self.setCentralWidget(central)

        # pages layout
        self.pageStack = QStackedLayout()

        # main GUI page
        mainPage = QWidget()
        # stack options vertically
        mainLayout = QVBoxLayout(mainPage)
        # buttons are stacked horizontally
        buttonsLayout = QHBoxLayout()
        # buttons
        self.listAgentsButton = QPushButton("List Agents")
        self.uploadDocumentsButton = QPushButton("Upload Documents")
        self.exitButton = QPushButton("Exit")

        # add to widget
        buttonsLayout.addWidget(self.listAgentsButton)
        buttonsLayout.addWidget(self.uploadDocumentsButton)
        buttonsLayout.addWidget(self.exitButton)
        # add to main layout at top
        mainLayout.addLayout(buttonsLayout)

        self.chat_output_one = QLabel()
        self.chat_output_two = QLabel()
        ####text display code

        self.horizontalGroupBox = QGroupBox()
        self.horizontalGroupBox.setStyleSheet("QGroupBox {border: none;}")
        #self.horizontalGroupBox.setStyleSheet("border: none;")
        #self.horizontalGroupBox.setStyleSheet('QGroupBox:title {subcontrol-origin: margin; subcontrol-position: top center;}')
        layout = QGridLayout()

        #second boxes to put inside of first box
        groupbox1 = QGroupBox("Details")
        groupbox1.setStyleSheet("QGroupBox {background-color: blue; margin-top: 40px; margin-right: 30px;}  QGroupBox::title {subcontrol-origin: margin; subcontrol-position: top center; margin-right: 30px;}")
        groupbox1_layout = QVBoxLayout()
        groupbox1_layout.addWidget(self.chat_output_one, alignment=Qt.AlignmentFlag.AlignTop)
        groupbox1.setLayout(groupbox1_layout)
        scroll = QScrollArea()
        scroll.setWidget(groupbox1)
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(300)

        groupbox2 = QGroupBox("Output")
        groupbox2.setStyleSheet("QGroupBox {background-color: red; margin-top: 40px; margin-left: 30px;}  QGroupBox::title {subcontrol-origin: margin; subcontrol-position: top center; margin-left: 30px;}")
        groupbox2_layout = QVBoxLayout()
        groupbox2_layout.addWidget(self.chat_output_two, alignment=Qt.AlignmentFlag.AlignTop)
        groupbox2.setLayout(groupbox2_layout)
        scroll2 = QScrollArea()
        scroll2.setWidget(groupbox2)
        scroll2.setWidgetResizable(True)
        scroll2.setFixedHeight(300)

        #layout.setColumnStretch(1, 4)
        #layout.setColumnStretch(2, 4)

        #chat_output_one = QLabel()
        #chat_output_two = QLabel()

        self.chat_output_one.setText("Chat output 1")
        self.chat_output_two.setText("Chat output 2")


        layout.addWidget(scroll,0,0)
        layout.addWidget(scroll2, 0, 1)
        #layout.addWidget(scroll_area)

        self.horizontalGroupBox.setLayout(layout)

        ####Add to main
        mainLayout.addWidget(self.horizontalGroupBox)

        ####text input code
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Type your message here...and press Enter key.")
        self.message_input.returnPressed.connect(self.send_message)

        mainLayout.addWidget(self.message_input)

        # Set the layout for the central widget
        #central_widget.setLayout(layout)

        # Initialize chat history
        self.chat_history = []
        '''

        HELLO JOEL GAMER !!!!!!!!
        YOU WOULD PUT YOUR STUFF HERE AND ADD TO THE MAIN LAYOUT


        *your code*
        mainLayout.addLayout(*name of your layout*)
        ETC !!!!!

        '''

        # user input
        #self.inputField = QLineEdit()
        #self.inputField.setPlaceholderText("Ask anything")
        # add to main layout below buttons
        #mainLayout.addWidget(self.inputField)

        # add main page to pages layout
        self.pageStack.addWidget(mainPage)

        '''LIST AGENTS PAGE'''
        self.listAgentsPage = QWidget()
        listAgentslayout = QVBoxLayout(self.listAgentsPage)
        # back button
        listAgentsBackButton = QPushButton("Back")
        # make shorter
        listAgentsBackButton.setMaximumWidth(100)
        # button functionality
        listAgentsBackButton.clicked.connect(self.showMain)
        # add to layout and align to the left
        listAgentslayout.addWidget(listAgentsBackButton, alignment=Qt.AlignmentFlag.AlignLeft)

        # text
        listAgentsTitle = QLabel("LIST OF AGENTS", alignment=Qt.AlignmentFlag.AlignHCenter)
        listAgentsTitle.setFont(QFont("", 24, QFont.Weight.Bold))
        listAgentslayout.addWidget(listAgentsTitle)
        self.pageStack.addWidget(self.listAgentsPage)

        '''UPLOAD DOCUMENTS PAGE'''
        self.uploadDocumentsPage = QWidget()
        uploadDocumentsLayout = QVBoxLayout(self.uploadDocumentsPage)

        # back button
        uploadDocumentsBackButton = QPushButton("Back")
        # make shorter
        uploadDocumentsBackButton.setMaximumWidth(100)
        # button functionality
        uploadDocumentsBackButton.clicked.connect(self.showMain)
        # add to layout and align to the left
        uploadDocumentsLayout.addWidget(uploadDocumentsBackButton, alignment=Qt.AlignmentFlag.AlignLeft)

        # select file
        uploadDocumentsTitle = QLabel("UPLOAD DOCUMENTS", alignment=Qt.AlignmentFlag.AlignHCenter)
        uploadDocumentsTitle.setFont(QFont("", 24, QFont.Weight.Bold))
        uploadDocumentsLayout.addWidget(uploadDocumentsTitle)

        uploadDocumentsLayout.setSpacing(5)
        uploadDocumentsLayout.setContentsMargins(10, 10, 10, 10)
        self.selectFileButton = QPushButton(" Select File")
        self.selectFileButton.setIcon(QIcon("folder.png"))
        self.selectFileButton.clicked.connect(self.selectFile)
        uploadDocumentsLayout.addWidget(self.selectFileButton, alignment=Qt.AlignmentFlag.AlignCenter)

        # doc list
        self.documentContainer = QWidget()
        self.documentListLayout = QVBoxLayout(self.documentContainer)
        self.documentListLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # scroll thing
        documentScroll = QScrollArea()
        documentScroll.setWidgetResizable(True)
        documentScroll.setFixedHeight(200)
        documentScroll.setWidget(self.documentContainer)

        # more scroll thing
        documentScrollBar = QScrollBar(Qt.Orientation.Vertical)
        documentScroll.setVerticalScrollBar(documentScrollBar)
        uploadDocumentsLayout.addWidget(documentScroll)

        # add layouts
        self.pageStack.addWidget(self.uploadDocumentsPage)

        # add functionality to main buttons
        self.listAgentsButton.clicked.connect(self.showListAgents)
        self.uploadDocumentsButton.clicked.connect(self.showUploadDocuments)
        self.exitButton.clicked.connect(QApplication.quit) # exit app

        central.setLayout(self.pageStack)

    # functions
    def showMain(self):
        self.pageStack.setCurrentIndex(0)

    def showListAgents(self):
        self.pageStack.setCurrentWidget(self.listAgentsPage)

    def showUploadDocuments(self):
        self.pageStack.setCurrentWidget(self.uploadDocumentsPage)

    def selectFile(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "Select Document")
        if filePath:
            print("File:", filePath)
            self.addDocument(filePath)

    def addDocument(self, filePath):
        row = QHBoxLayout()
        label = QLabel(filePath)
        label.setWordWrap(True)

        # button
        removeButton = QPushButton()
        removeButton.setIcon(QIcon("bin.png"))
        removeButton.setMaximumWidth(30)

        container = QWidget()
        container.setLayout(row)

        # remove file row
        def removeRow():
            container.setParent(None)
            container.deleteLater()
        removeButton.clicked.connect(removeRow)

        row.addWidget(label)
        row.addStretch()
        row.addWidget(removeButton)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        self.documentListLayout.addWidget(line)
        self.documentListLayout.addWidget(container)

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
        self.createGridLayout()
        self.show()

    def createGridLayout(self):
        self.horizontalGroupBox = QGroupBox()
        self.horizontalGroupBox.setStyleSheet("QGroupBox {border: none;}")
        #self.horizontalGroupBox.setStyleSheet("border: none;")
        #self.horizontalGroupBox.setStyleSheet('QGroupBox:title {subcontrol-origin: margin; subcontrol-position: top center;}')
        layout = QGridLayout()

        #second boxes to put inside of first box
        groupbox1 = QGroupBox("Details")
        groupbox1.setStyleSheet("QGroupBox {background-color: blue; margin-top: 20px; margin-right: 30px;}  QGroupBox::title {subcontrol-origin: margin; subcontrol-position: top center; margin-right: 30px;}")
        groupbox1_layout = QVBoxLayout()
        groupbox1_layout.addWidget(self.chat_output_one, alignment=Qt.AlignmentFlag.AlignTop)
        groupbox1.setLayout(groupbox1_layout)
        scroll = QScrollArea()
        scroll.setWidget(groupbox1)
        scroll.setWidgetResizable(True)
        scroll.setFixedHeight(300)

        groupbox2 = QGroupBox("Output")
        groupbox2.setStyleSheet("QGroupBox {background-color: red; margin-top: 20px; margin-left: 30px;}  QGroupBox::title {subcontrol-origin: margin; subcontrol-position: top center; margin-left: 30px;}")
        groupbox2_layout = QVBoxLayout()
        groupbox2_layout.addWidget(self.chat_output_two, alignment=Qt.AlignmentFlag.AlignTop)
        groupbox2.setLayout(groupbox2_layout)
        scroll2 = QScrollArea()
        scroll2.setWidget(groupbox2)
        scroll2.setWidgetResizable(True)
        scroll2.setFixedHeight(300)

        #layout.setColumnStretch(1, 4)
        #layout.setColumnStretch(2, 4)

        #chat_output_one = QLabel()
        #chat_output_two = QLabel()

        self.chat_output_one.setText("Chat output 1")
        self.chat_output_two.setText("Chat output 2")


        layout.addWidget(scroll,0,0)
        layout.addWidget(scroll2, 0, 1)
        #layout.addWidget(scroll_area)

        self.horizontalGroupBox.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    #app.setStyle("Fusion")
    window = MainWindow()
    window.resize(700, 500)
    apply_stylesheet(app, theme='light_red.xml',)
    window.show()
    sys.exit(app.exec())
