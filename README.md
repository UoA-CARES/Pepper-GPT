# Pepper-GPT (Project 91)

## Project Name

Investigating the Integration of Pepper Robot and ChatGPT: A Study on Enhancing User Experience and Engagement.



## Introduction

Pepper-GPT is an integration system with the Whisper Small Model and gpt-3.5-turbo embedded into the Pepper robot for user experience enhancement.



## Installation

Pepper-GPT consists of two programs: **Black Box** and **Pepper Controller**, which require a connection between these two programs.



### Network Settings

The Pepper robot in the robotics lab connects to a private WiFi, which needs to connect via a VPN. To avoid complications, **Black Box** runs in Python 3 in Windows 11. And **Pepper Controller** is running in Python 2.7 in Ubuntu 20.04 with the VPN.

To connect the Black Box client, open a terminal in Linux and input:

`sudo ip route`
`sudo ip route add 172.22.1.21/32 dev vpn`

This will list out all the ip route. Then delete all the other `ip route` with the word "`vpn`":

e.g. `sudo ip route del 10.0.0.0/8`



### Environment Settings

Before running the programs, make sure the device is with a GPU. 

All the libraries are listed in the requirements.txt file. Use the command:

`pip install -r requirements.txt`

#### Naoqi SDK Installation

The installation for the Pepper robot's python SDK (Naoqi 2.5 SDK) should following the steps below:

`source ~/naoqi.sh # Install naoqi SDK`

`~/naoqi/naoqi-sdk-2.1.4.13-linux64/naoqi # Check the installation by executing NAOqi`

"""
You should see an output similar to:

Starting NAOqi version 2.1.4.13
.
NAOqi is listening on 0.0.0.0:9559
.
.
NAOqi is ready...
Press CTRL-C to exit.
"""



#### Naoqi Environment Configuration

`gedit ~/.bashrc # config the environment, write following content at the end of the document`

`alias python='/usr/bin/python2.7'`
`export PYTHONPATH=${PYTHONPATH}:~/naoqi/pynaoqi-python2.7-2.1.4.13-linux64`
`export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:~/naoqi/pynaoqi-python2.7-2.1.4.13-linux64`

`source ~/.bashrc # activate the new configuration`

"""
if there is an error of "`ImportError:libboost_regex.so.1.55.0:cannot open shared object file: No such file or directory` "
use the command "`locate libboost_regex.so.1.55.0`" find its path
open the path, find this file and copy it to the **LD_LIBRARY_PATH**

"""



## Running

1. Install the programs into different systems (**Black Box** in Win 11;  **Pepper Controller** in Ubuntu 20.04)
2. Run the VPN.
3. Set the network according to the section **Network Settings**
4. Run the `server.py` file in Ubuntu for starting
5. Run the `main.py` file in Ubuntu for opening the client of **Pepper Controller**
6. Run the `main.py` file in Windows for opening the client of **Black Box**
7. If the terminal print out the information "`Press Enter to Start.`", then the project runs successfully.