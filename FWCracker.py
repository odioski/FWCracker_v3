import os
import subprocess
import sys
import time
import serial

#   Needed for flow 


#   Needed to run the helper code


#   Qt6 needs this and the following...

basedir = os.path.dirname(__file__)


from PyQt6.QtCore import QObject, QRunnable, QSize, Qt, QThreadPool
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import (QApplication, QCheckBox, QLabel, QLineEdit,
                             QMainWindow, QPushButton, QVBoxLayout, QWidget)

#   Necessary components...


global bios_state
bios_state = "NIL"

#   From here we'll attempt to integrate a workable GUI for this app


app = QApplication(sys.argv)


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

        word.setPlaceholderText("Enter the word or phrase here...")
        word.textChanged.connect(self.decouple_word)

        pattern.setPlaceholderText("Enter the number portion here...")
        pattern.textChanged.connect(self.decouple_pattern)


        port.setPlaceholderText("Enter your serial port here. Should be something like COM* or /dev/tty/USB*...")
        port.textChanged.connect(self.decouple_port)
        
        
        bios_state = QCheckBox("Bios needs confirmation?")
        bios_state.stateChanged.connect(self.decouple_bios_state)

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
        layout.addWidget(bios_state)
        layout.addWidget(findPorts)
        layout.addWidget(SerialLabel)
        layout.addWidget(port)
        layout.addWidget(launchButton)

        container = QWidget()
        container.setLayout(layout)

        #self.setFixedSize(QSize(###, 400))

        self.setCentralWidget(container)

#   That's it,


#   Some helpers...

    def decouple_word(self, text):
        global some_word
        some_word = text
    
    def decouple_pattern(self, text):
        global global_number_pattern
        if text.isdecimal() == False:
            print("Need a number here...")
        else:
            global_number_pattern = text
    
    def decouple_bios_state(self, state):
        if state > 0:
            bios_state = "SET"
            print("Bios Confirmation: " + bios_state)
        else:
            bios_state = "UNSET"
            print("Bios Confirmation: " + bios_state)
    
    def decouple_port(self, text):
        global hid_port
        hid_port = text

    def starter(self):
        QThreadPool.globalInstance().start(self.build_range)
        print("\n Welcome " + os.name)


#   FWCracker, modified
    

    def build_range(self):
        control = bios_state
        known_factor = int(global_number_pattern) / 10
        keep = ""
        if known_factor <= 1:
            o_range = 10
            print("\n10 different possibilities based on this info...\n")
            keep = 'Y'
        else:
            if known_factor <= 10:
                o_range = 100
                print("\n100 different possiblities based on this info...\n")
                keep = 'Y'
            else:
                if known_factor <= 100:
                    o_range = 1000
                    print("\n1,000 different possiblities based on this info...\n")
                    keep = 'Y'
                else:
                    if known_factor <= 1000:
                        o_range = 10000
                        print("\n10,000 different possiblities based on this info...\n")
                        keep = 'Y'
                    else:
                        if known_factor <= 10000:
                            o_range = 100000
                            print("\nBased on the number you provided this will take a very long time.\n")
                            keep = 'Y'
                        else:
                            if known_factor <= 100000:
                                o_range = 1000000
                                print("\nPractically impossible, theoretically....might as well continue...")
                                keep = 'Y'
                            else:
                                if known_factor <= 1000000:
                                    o_range = 1000000
                                    print("\nOkey dokey...")
                                    keep = 'Y'
        set_range = o_range
        time.sleep(3)
        build_passcode(some_word, control,  set_range)


def build_passcode(some_word, control, set_range):
    n = 1
    while n <= set_range:
        passcode = some_word + str(n)
        to_bytes = passcode.encode(encoding='ascii')
        do_writer_do(to_bytes, n, passcode, control, set_range)
        n += 1
    print("Later...")

    
def do_writer_do(to_bytes, n, passcode, control, set_range):
    print("This is attempt #" + str(n) + " of " + str(set_range) + ", using this password: " + passcode)
    time.sleep(1)
    space = "\n"

    ser = serial.Serial(hid_port)
    ser.baudrate = 9600

    space_to_bytes = space.encode(encoding='ascii')
    ser.write(to_bytes)
    time.sleep(1)

    if str(control) == 'SET':
        print('\n')
        ser.write(space_to_bytes)
    int(n)
    int(set_range)
    time.sleep(2)       
        

def find_ports():
    if os.name == "nt":
        code = "pyserial-ports.exe -v"
    elif os.name == "posix":
        code = "pyserial-ports -v"
    subprocess.run(code)


window = MainWindow()
window.show()


app.exec()


#   FWCracker_v3...
