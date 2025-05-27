#tutorial 1
'''
import sys

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton


# Subclass QMainWindow to customize your application's main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        button = QPushButton("Press Me!")

        self.setFixedSize(QSize(400, 300))

        # Set the central widget of the Window.
        self.setCentralWidget(button)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
'''
#tutorial 2
'''
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton

import sys
from random import choice

window_titles = [
    'My App',
    'My App',
    'Still My App',
    'Still My App',
    'What on earth',
    'What on earth',
    'This is surprising',
    'This is surprising',
    'Something went wrong'
]


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.n_times_clicked = 0

        self.setWindowTitle("My App")

        self.button = QPushButton("Press Me!")
        self.button.clicked.connect(self.the_button_was_clicked)

        self.windowTitleChanged.connect(self.the_window_title_changed)

        # Set the central widget of the Window.
        self.setCentralWidget(self.button)

    def the_button_was_clicked(self):
        print("Clicked.")
        new_window_title = choice(window_titles)
        print("Setting title:  %s" % new_window_title)
        self.setWindowTitle(new_window_title)

    def the_window_title_changed(self, window_title):
        print("Window title changed: %s" % window_title)

        if window_title == 'Something went wrong':
            self.button.setDisabled(True)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
'''
#tutorial 2.2
'''
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QWidget

import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        self.label = QLabel()

        self.input = QLineEdit()
        self.input.textChanged.connect(self.label.setText)

        layout = QVBoxLayout()
        layout.addWidget(self.input)
        layout.addWidget(self.label)

        container = QWidget()
        container.setLayout(layout)

        # Set the central widget of the Window.
        self.setCentralWidget(container)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
'''
#tutorial 3
'''
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDial,
    QDoubleSpinBox,
    QLabel,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QSlider,
    QSpinBox,
)

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        widget = QLabel("Hello")
        font = widget.font()
        font.setPointSize(30)
        widget.setFont(font)
        widget.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        self.setCentralWidget(widget)
        widget.setPixmap(QPixmap('kitchen2.png'))

app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()
'''
#tutorial 4
'''
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QLabel,
    QMainWindow,
    QStatusBar,
    QToolBar,
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")

        label = QLabel("Hello!")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setCentralWidget(label)

        toolbar = QToolBar("My main toolbar")
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)

        button_action = QAction(QIcon("bug.png"), "&Your button", self)
        button_action.setStatusTip("This is your button")
        button_action.triggered.connect(self.toolbar_button_clicked)
        button_action.setCheckable(True)
        toolbar.addAction(button_action)

        toolbar.addSeparator()

        button_action2 = QAction(QIcon("bug.png"), "Your &button2", self)
        button_action2.setStatusTip("This is your button2")
        button_action2.triggered.connect(self.toolbar_button_clicked)
        button_action2.setCheckable(True)
        toolbar.addAction(button_action2)

        toolbar.addWidget(QLabel("Hello"))
        toolbar.addWidget(QCheckBox())

        self.setStatusBar(QStatusBar(self))

    def toolbar_button_clicked(self, s):
        print("click", s)

app = QApplication([])
window = MainWindow()
window.show()
app.exec()
'''
#layout testing
'''
import sys

from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QStackedLayout,
    QVBoxLayout,
    QWidget,
)

from layout_colourwidget import Color


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")

        pagelayout = QVBoxLayout()
        button_layout = QHBoxLayout()
        self.stacklayout = QStackedLayout()

        pagelayout.addLayout(button_layout)
        pagelayout.addLayout(self.stacklayout)

        btn = QPushButton("red")
        btn.pressed.connect(self.activate_tab_1)
        button_layout.addWidget(btn)
        self.stacklayout.addWidget(Color("red"))

        btn = QPushButton("green")
        btn.pressed.connect(self.activate_tab_2)
        button_layout.addWidget(btn)
        self.stacklayout.addWidget(Color("green"))

        btn = QPushButton("yellow")
        btn.pressed.connect(self.activate_tab_3)
        button_layout.addWidget(btn)
        self.stacklayout.addWidget(Color("yellow"))

        widget = QWidget()
        widget.setLayout(pagelayout)
        self.setCentralWidget(widget)

    def activate_tab_1(self):
        self.stacklayout.setCurrentIndex(0)

    def activate_tab_2(self):
        self.stacklayout.setCurrentIndex(1)

    def activate_tab_3(self):
        self.stacklayout.setCurrentIndex(2)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
'''
#Final test
'''
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QLabel,
    QMainWindow,
    QStatusBar,
    QToolBar,
    QVBoxLayout,
    QHBoxLayout,
    QStackedLayout,
    QLineEdit,
    QWidget,
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("The test")
        #currently pagelayout is uselsess
        pagelayout = QVBoxLayout()
        button_layout = QHBoxLayout()
        self.stacklayout = QStackedLayout()

        pagelayout.addLayout(button_layout)
        pagelayout.addLayout(self.stacklayout)

        self.label = QLabel("Hello!")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setCentralWidget(self.label)

        toolbar = QToolBar("My main toolbar")
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)

        button_action = QAction(QIcon("bug.png"), "&Your button", self)#can change button to an immage
        button_action.setStatusTip("This is your button")
        button_action.triggered.connect(self.toolbar_button_clicked)
        #button_action.setCheckable(True)
        toolbar.addAction(button_action)

        toolbar.addSeparator()

        button_action2 = QAction(QIcon("bug.png"), "Your &button2", self)
        button_action2.setStatusTip("This is your button2")
        button_action2.triggered.connect(self.toolbar_button_clicked2)
        #button_action2.setCheckable(True)
        toolbar.addAction(button_action2)

        button_action = QAction(QIcon("bug.png"), "&Your button", self)#can change button to an immage
        button_action.setStatusTip("This is your button3")
        button_action.triggered.connect(self.toolbar_button_clicked3)
        button_action.setCheckable(True)
        toolbar.addAction(button_action)

        toolbar.addSeparator()

        button_action = QAction(QIcon("bug.png"), "&Your button", self)#can change button to an immage
        button_action.setStatusTip("This is your button4")
        button_action.triggered.connect(self.toolbar_button_clicked4)
        button_action.setCheckable(True)
        toolbar.addAction(button_action)

        toolbar.addSeparator()

        button_action = QAction(QIcon("bug.png"), "&Your button", self)#can change button to an immage
        button_action.setStatusTip("This is your button5")
        button_action.triggered.connect(self.toolbar_button_clicked5)
        button_action.setCheckable(True)
        toolbar.addAction(button_action)

        toolbar.addSeparator()

        button_action = QAction(QIcon("bug.png"), "&Your button", self)#can change button to an immage
        button_action.setStatusTip("This is your button6")
        button_action.triggered.connect(self.toolbar_button_clicked6)
        button_action.setCheckable(True)
        toolbar.addAction(button_action)

        self.setStatusBar(QStatusBar(self))

        self.text_input = QLineEdit()
        self.text_input.textChanged.connect(self.text_input_proccess)
        self.text_input.returnPressed.connect(self.enter_click)
        text_input_layout = QVBoxLayout()
        text_input_layout.addWidget(self.text_input)
        text_input_layout.addWidget(self.label)

        container = QWidget()
        container.setLayout(text_input_layout)

        # Set the central widget of the Window.
        self.setCentralWidget(container)

    def text_input_proccess(self):
        print("The text input is -->", self.text_input.text())

    def enter_click(self):
        self.label.setText(self.text_input.text())

    def toolbar_button_clicked(self, s):
        print("click", s)
        self.label.setText("Updated OMG so cool")

    def toolbar_button_clicked2(self, s):
        print("click", s)
        self.label.setText("Definetly")

    def toolbar_button_clicked3(self, s):
        print("click", s)
        self.label.setText("3")

    def toolbar_button_clicked4(self, s):
        print("click", s)
        self.label.setText("4")

    def toolbar_button_clicked5(self, s):
        print("click", s)
        self.label.setText("5")

    def toolbar_button_clicked6(self, s):
        print("click", s)
        self.label.setText("Aiden!")



app = QApplication([])
window = MainWindow()
window.show()
app.exec()
'''
#changing windows
'''
import sys

from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QTabWidget Example")
        self.resize(270, 110)
        # Create a top-level layout
        layout = QVBoxLayout()
        self.setLayout(layout)
        # Create the tab widget with two tabs
        tabs = QTabWidget()
        tabs.addTab(self.generalTabUI(), "General")
        tabs.addTab(self.networkTabUI(), "Network")
        layout.addWidget(tabs)

    def generalTabUI(self):
        """Create the General page UI."""
        generalTab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QCheckBox("General Option 1"))
        layout.addWidget(QCheckBox("General Option 2"))
        generalTab.setLayout(layout)
        return generalTab

    def networkTabUI(self):
        """Create the Network page UI."""
        networkTab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QCheckBox("Network Option 1"))
        layout.addWidget(QCheckBox("Network Option 2"))
        networkTab.setLayout(layout)
        return networkTab

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
'''
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
        self.setGeometry(100, 100, 400, 300)  # (x, y, width, height)

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
