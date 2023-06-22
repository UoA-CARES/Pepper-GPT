#!/bin/bash

gnome-terminal -t "server" -x bash -c "cd PycharmProjects/BlackBox/;
python3 server.py;
exec bash"
sleep 1s

gnome-terminal -t "BlackBox_Client" -x bash -c "cd PycharmProjects/BlackBox/;
python3 main.py;
exec bash"
sleep 1s

gnome-terminal -t "PepperController_Client" -x bash -c "cd PycharmProjects/PepperController/;
python2 client.py;
exec bash"
