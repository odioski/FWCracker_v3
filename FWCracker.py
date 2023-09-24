import os
import subprocess
import sys
import time
import serial


basedir = os.path.dirname(__file__)

from pathlib import Path

from PyQt6.QtCore import QObject, QRunnable, QSize, Qt, QThreadPool
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import (QApplication, QCheckBox, QLabel, QLineEdit,
                             QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget)

#   Necessary components...

global newData


#   From here we'll attempt to integrate a workable GUI for this app


app = QApplication([])

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

    
        logo = QLabel("FWCracker")
        logo.setPixmap(QPixmap(os.path.join(basedir, "logo.png")))
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        PhraseLabel = QLabel("Word/Phrase")
        NumberLabel = QLabel("Number")
        SerialLabel = QLabel("Serial Port")

        word = QLineEdit()
        pattern = QLineEdit()
        port = QLineEdit()
      
        Progress = QLabel("Progress")
        Progress.setAlignment(Qt.AlignmentFlag.AlignCenter)

        
        word.setPlaceholderText("Enter the word or phrase here...")
        word.textChanged.connect(self.decouple_word)

        pattern.setPlaceholderText("Enter the number portion here...")
        pattern.textChanged.connect(self.decouple_pattern)

        port.setPlaceholderText("Enter your serial port here. Should be something like COM# or /dev/tty/USB##...")
        port.textChanged.connect(self.decouple_port)
        
        
        control = QCheckBox("Bios needs confirmation?")
        control.stateChanged.connect(self.decouple_control)


        launchButton = QPushButton("Launch")
        launchButton.setFixedHeight(30)
        launchButton.clicked.connect(self.starter)


        global pauseButton

        pauseButton = QPushButton()
        pauseButton.setIcon(QIcon(os.path.join(basedir, "pauseBtn.png")))
        pauseButton.setFixedSize(30, 30)

        global Output

        Output = QLabel("Output will be displayed here...")
        Output.setObjectName("nfo")
        Output.setFixedHeight(250)
        Output.setAlignment(Qt.AlignmentFlag.AlignCenter)
        Output.setWordWrap(True)

              
        findPorts = QPushButton("List Ports")
        findPorts.clicked.connect(find_ports)

        layout = QVBoxLayout()
        app_controls = QHBoxLayout()

        layout.addWidget(logo)
        layout.addWidget(PhraseLabel)
        layout.addWidget(word)
        layout.addWidget(NumberLabel)
        layout.addWidget(pattern)
        layout.addWidget(control)
        layout.addWidget(findPorts)
        layout.addWidget(SerialLabel)
        layout.addWidget(port)

        layout.addLayout(app_controls)

        app_controls.addWidget(launchButton)
        app_controls.addWidget(pauseButton)

        layout.addWidget(Output)

        app_container = QWidget()
        app_container.setLayout(layout)

#   self.setFixedSize(QSize(###, 400))

        self.setCentralWidget(app_container)

#   That's it, thanks to py(Qt)


#   Some helpers...

    def decouple_word(self, text):
        global some_word
        some_word = text
    
    def decouple_pattern(self, text):
        global global_number_pattern
        if text.isdecimal() == False:
            newData = "Need a number here..."
            update_results(newData)
        else:
            global_number_pattern = text
    
    def decouple_control(self, state):
        global control
        if state > 0:
            control = "SET"
            newData = "Bios Confirmation: " + control
            update_results(newData)
        else:
            control = "UNSET"
            newData = "Bios Confirmation: " + control
            update_results(newData)
#           return(control)
            
    def decouple_port(self, text):
        global hid_port
        hid_port = text

    def starter(self):
        QThreadPool.globalInstance().start(self.build_range)


#   FWCracker, modified
    

    def build_range(self):
        newData = "\nWelcome " + os.name + " user..."
        update_results(newData)
        time.sleep(3)
        known_factor = int(global_number_pattern) / 10
        
        if known_factor <= 1:
            o_range = 10
            newData = "\n10 different possibilities based on this info...\n"
            update_results(newData)
            
        else:
            if known_factor <= 10:
                o_range = 100
                newData = "\n100 different possiblities based on this info...\n"
                update_results(newData)
                
            else:
                if known_factor <= 100:
                    o_range = 1000
                    newData = "\n1,000 different possiblities based on this info...\n"
                    update_results(newData)
                    
                else:
                    if known_factor <= 1000:
                        o_range = 10000
                        newData = "\n10,000 different possiblities based on this info...\n"
                        update_results(newData)
                        
                    else:
                        if known_factor <= 10000:
                            o_range = 100000
                            newData = "\nBased on the number you provided this will take a very long time.\n"
                            update_results(newData)
                            
                        else:
                            if known_factor <= 100000:
                                o_range = 1000000
                                newData = "\nPractically impossible, theoretically....might as well continue..."
                                update_results(newData)
                                
                            else:
                                if known_factor <= 1000000:
                                    o_range = 1000000
                                    newData = "\nOkey dokey..."
                                    update_results(newData)
                                    
        set_range = o_range
        time.sleep(3)
        build_passcode(some_word, control, set_range)


def build_passcode(some_word, control, set_range):
    n = 1
    while n <= set_range:
        passcode = some_word + str(n) + "\n"
        to_bytes = passcode.encode(encoding='ascii')
        do_writer_do(to_bytes, n, passcode, control, set_range)
        n += 1

        if pauseButton.changeEvent:
            break
            FWCracker_status = "FWCracker is paused..."
            newData = FWCracker_status
            update_results(newData)
        elif pauseButton.changeEvent:
            continue

    ser = serial.Serial(hid_port)
    ser.baudrate = 9600

    newData = "Later..."
    update_results(newData)
    quit()

    
def do_writer_do(to_bytes, n, passcode, control, set_range):
    
    newData = "Completed attempt #" + str(n) + " of " + str(set_range) + ", using password: " + passcode 
       
    time.sleep(1)
    space = "\n\n"

    ser = serial.Serial(hid_port)
    ser.baudrate = 9600

    space_to_bytes = space.encode(encoding='ascii')
    ser.write(to_bytes)
    time.sleep(1)

    update_results(newData)
    
    if str(control) == 'SET':
        ser.write(space_to_bytes)
    int(n)
    int(set_range)
    time.sleep(2) 


def installer():
        check_online = 'ping yahoo.com'
        online = subprocess.getstatusoutput(check_online)
        status = online[0]
        ping_output = online[1]
        newData = ping_output
        update_results(newData)

        if status > 0:
            install = 'pip install pyserial'
            newData = subprocess.getoutput(install)
            update_results(newData)
            time.sleep(3)
        else:
            newData = "FWCracker needs to be online to get pyserial. Connect to the internet and restart app."
            update_results(newData)
            time.sleep(5)
            quit()      
        


def find_ports():
    pyserial_exists = 'pyserial-ports'
    check = subprocess.getstatusoutput(pyserial_exists)[0]
    if check > 0:
        installer()
    code = 'pyserial-ports -v'
    newData = subprocess.getoutput(code)
    update_results(newData) 


def update_results(newData):
    Output.setText(newData)


#   Launch pyQt app...


window = MainWindow()
window.show()

app.setStyleSheet(Path(os.path.join(basedir, 'FWCracker.qss')).read_text())
app.exec()


#   FWCracker_v3...