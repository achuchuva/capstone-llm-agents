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
    QStackedLayout
)
from PyQt6.QtCore import Qt

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

        # user input
        self.inputField = QLineEdit()
        self.inputField.setPlaceholderText("Ask anything")
        # add to main layout below buttons
        mainLayout.addWidget(self.inputField)

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
        listAgentslayout.addWidget(QLabel("List of agents", alignment=Qt.AlignmentFlag.AlignCenter))
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
        # text
        uploadDocumentsLayout.addWidget(QLabel("Upload your documents", alignment=Qt.AlignmentFlag.AlignCenter))
        self.pageStack.addWidget(self.uploadDocumentsPage)

        # add functionality to buttons
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    # window.resize(width, height)
    window.show()
    sys.exit(app.exec())
