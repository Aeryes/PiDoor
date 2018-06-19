# PiDoor
This project allows the user to construct a device to track traffic in and out of doors. The project uses PiZero and Python 2.7. This project was made during my time in the USAF and will save money and man hours for the installation I was assigned too.

The project uses a state machine to cycle through availble menus. This state system was designed in such a way to make the creation of additional menus an easy and straight forward task. In order to construct this device you will need the following componenets:

- PiZero
- Papirus Epaper for PiZero
- Hall effect sensor
- 2 Led lights of different color
- Wire for AC, Ground and Input/Output
- Electrical tape
- Case using a 3D printer is optional
- Battery pack or solar panels are optional. (Wired power could be used)

The Led lights are assigned to GPIO.BCM pins as follows:
Hall effect sensor - Pin 4
Red Led - Pin 22
Green Led - Pin 27

The attached pictures show what an uncased project would look like upon completion. 

### Actual Project:

![alt text](https://github.com/Aeryes/PiDoor/blob/master/Project%20Images/actualproject.jpg)

### Case Sample without top:

![alt text](https://i.imgur.com/h33OSPK.jpg)
![alt text](https://i.imgur.com/YEo7sbK.jpg)

After putting the project together all that you need to do is have both scripts run on startup. You can do this by opening up a new terminal and adding the files to crontab using the full paths.

This is my first fully completed Raspberry Pi project. I hope you enjoy it.
