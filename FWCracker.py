import os
import subprocess
import sys
import time
import serial


basedir = os.path.dirname(__file__)


from PyQt6.QtCore import QObject, QRunnable, QSize, Qt, QThreadPool
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import (QApplication, QCheckBox, QLabel, QLineEdit,
                             QMainWindow, QPushButton, QVBoxLayout, QWidget)

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

        global Output

        Output = QLabel("Output will be displayed here...")
        Output.setObjectName("out")
        Output.setFixedHeight(300)
        Output.setAlignment(Qt.AlignmentFlag.AlignCenter)
        Output.setWordWrap(True)
        
        word.setPlaceholderText("Enter the word or phrase here...")
        word.textChanged.connect(self.decouple_word)

        pattern.setPlaceholderText("Enter the number portion here...")
        pattern.textChanged.connect(self.decouple_pattern)


        port.setPlaceholderText("Enter your serial port here. Should be something like COM# or /dev/tty/USB##...")
        port.textChanged.connect(self.decouple_port)
        
        
        control = QCheckBox("Bios needs confirmation?")
        control.stateChanged.connect(self.decouple_control)

        launchButton = QPushButton("Launch")
        
        launchButton.clicked.connect(self.starter)

              
        findPorts = QPushButton("List Ports")
        findPorts.clicked.connect(find_ports)

        layout = QVBoxLayout()
        layout.addWidget(logo)
        layout.addWidget(PhraseLabel)
        layout.addWidget(word)
        layout.addWidget(NumberLabel)
        layout.addWidget(pattern)
        layout.addWidget(control)
        layout.addWidget(findPorts)
        layout.addWidget(SerialLabel)
        layout.addWidget(port)
        layout.addWidget(launchButton)
        layout.addWidget(Output)

        container = QWidget()
        container.setLayout(layout)

        #self.setFixedSize(QSize(###, 400))

        self.setCentralWidget(container)

#   That's it, thanks to Qt


#   Some helpers...

    def decouple_word(self, text):
        global some_word
        some_word = text
    
    def decouple_pattern(self, text):
        global global_number_pattern
        if text.isdecimal() == False:
            newData = "Need a number here..."
            results(newData)
        else:
            global_number_pattern = text
    
    def decouple_control(self, state):
        global control
        if state > 0:
            control = "SET"
            newData = "Bios Confirmation: " + control
            results(newData)
        else:
            control = "UNSET"
            newData = "Bios Confirmation: " + control
            results(newData)
        return(control)
            
    def decouple_port(self, text):
        global hid_port
        hid_port = text

    def starter(self):
        QThreadPool.globalInstance().start(self.build_range)


#   FWCracker, modified
    

    def build_range(self):
        newData = "\nWelcome " + os.name + " user..."
        results(newData)
        time.sleep(3)
        known_factor = int(global_number_pattern) / 10
        
        if known_factor <= 1:
            o_range = 10
            newData = "\n10 different possibilities based on this info...\n"
            results(newData)
            
        else:
            if known_factor <= 10:
                o_range = 100
                newData = "\n100 different possiblities based on this info...\n"
                results(newData)

                
            else:
                if known_factor <= 100:
                    o_range = 1000
                    newData = "\n1,000 different possiblities based on this info...\n"
                    results(newData)
                    
                else:
                    if known_factor <= 1000:
                        o_range = 10000
                        newData = "\n10,000 different possiblities based on this info...\n"
                        results(newData)
                        
                    else:
                        if known_factor <= 10000:
                            o_range = 100000
                            newData = "\nBased on the number you provided this will take a very long time.\n"
                            results(newData)
                            
                        else:
                            if known_factor <= 100000:
                                o_range = 1000000
                                newData = "\nPractically impossible, theoretically....might as well continue..."
                                results(newData)
                                
                            else:
                                if known_factor <= 1000000:
                                    o_range = 1000000
                                    newData = "\nOkey dokey..."
                                    results(newData)
                                    
        set_range = o_range
        time.sleep(3)
        build_passcode(some_word, control, set_range, newData)


def build_passcode(some_word, control, set_range, newData):
    n = 1
    while n <= set_range:
        passcode = some_word + str(n) + "\n"
        to_bytes = passcode.encode(encoding='ascii')
        do_writer_do(to_bytes, n, passcode, control, set_range)
        n += 1

    ser = serial.Serial(hid_port)
    ser.baudrate = 9600

    newData = "Later..."
    results(newData)
    quit()

    
def do_writer_do(to_bytes, n, passcode, control, set_range):

    global newData
    
    newData = "Completed attempt #" + str(n) + " of " + str(set_range) + ", using password: " + passcode 
       
    time.sleep(1)
    space = "\n\n"

    ser = serial.Serial(hid_port)
    ser.baudrate = 9600

    space_to_bytes = space.encode(encoding='ascii')
    ser.write(to_bytes)
    time.sleep(1)

    results(newData)
    
    if str(control) == 'SET':
        ser.write(space_to_bytes)
    int(n)
    int(set_range)
    time.sleep(2) 


def installer():
        check_online = 'ping yahoo.com'
        online = subprocess.getstatusoutput(check_online)
        newData = str(online)
        results(newData)
        if online == 0:
            install = 'pip install pyserial'
            newData = subprocess.getoutput(install)
            results(newData)
            time.sleep(3)
        else:
            newData = "FWCracker needs to be online to get pyserial. Connect to internet and restart app."
            time.sleep(5)
            quit()      
        


def find_ports():
    pyserial_exists = 'pyserial-ports'
    check = subprocess.getstatusoutput(pyserial_exists)[0]
    if check > 0:
        installer()
    code = 'pyserial-ports -v'
    newData = subprocess.getoutput(code)
    results(newData) 


def results(newData):
    Output.setText(newData)


#   Launch pyQt app...


window = MainWindow()
window.show()


app.exec()


#   FWCracker_v3...