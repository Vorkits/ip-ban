#!/bin/bash
papath=`pwd`
echo $papath
#echo "${BASH_SOURCE[0]}"
#dirname "${BASH_SOURCE[0]}"

sudo apt update
echo yes | sudo apt-get --fix-missing  install build-essential autoconf libtool pkg-config python-opengl python-imaging python-pyrex python-pyside.qtopengl idle-python2.7 qt4-dev-tools qt4-designer libqtgui4 libqtcore4 libqt4-xml libqt4-test libqt4-script libqt4-network libqt4-dbus python-qt4 python-qt4-gl libgle3 python-dev
echo yes | sudo apt-get --fix-missing install python3-pip
pip3 install -r requirements.txt
sed -i 's|dir|'$papath'|g' ban.service 
cp -r ban.service /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl enable ban.service
sudo systemctl start ban.service
