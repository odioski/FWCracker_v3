#   FWCracker_v3 w/GUI

Same as version 2 with more ease of use in deployment. 

You can launch the GUI from the terminal or run the exe in /dist

For more about FWCracker visit, *https://github.com/odioski/FWCracker_v2*

![Mine](https://github.com/user-attachments/assets/7dd04b42-3054-44d8-82b9-199d3ec671be)

#	INSTALLATION
A few options...

#	Use Python

Download the code:
	
	git clone https://github.com/odioski/FWCracker_v3.git

Get PySerial and pyQt6
	
	pip install pyserial pyQt6

Run FWCracker

	python FWCracker.py

#	Launch the Win .exe

Download the code:

	git clone https://github.com/odioski/FWCracker_v3.git

Navigate to /dist inside is FWCracker.exe


#	Install FWCracker

Download the code:

	git clone https://github.com/odioski/FWCracker_v3.git

Run the FWCracker_v3_Installer located in /INSTALLER

Launch FWCracker from your Desktop

#	Build your own

Download the code:

	git clone https://github.com/odioski/FWCracker_v3.git

Download PyInstaller and pyQt6 if you don't already have those:

	pip install pyinstaller pyQt6

Use Pyinstaller and the .spec:

	pyinstaller FWCracker.spec

 Inside /dist you'll find FWCracker.exe


# SUPPORT

FWCracker_v3 will *install* pyserial if not on the system.

If FWCracker can't find pyserial-ports you can add it to your *PATH*. From there, find your port in the Device Manager and launch.

As in previous versions you'll need a serial to hid keyboard emulator. 

You can see what one looks like by visiting *https://tinyurl.com/5xe4n4mn*
