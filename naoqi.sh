#! /bin/bash
# this is the installation file for Naoqi on Ubuntu
echo "create the path"
mkdir -p ~/naoqi
cd ~/naoqi

echo "Start downloading SDK"
wget https://community-static.aldebaran.com/resources/2.1.4.13/sdk-c%2B%2B/naoqi-sdk-2.1.4.13-linux64.tar.gz
wget https://community-static.aldebaran.com/resources/2.1.4.13/sdk-python/pynaoqi-python2.7-2.1.4.13-linux64.tar.gz # if you are using 64-bit
tar xzf naoqi-sdk-2.1.4.13-linux64.tar.gz
tar xzf pynaoqi-python2.7-2.1.4.13-linux64.tar.gz # if you are using 64-bit