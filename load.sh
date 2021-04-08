#!/bin/bash
service_file=`cat ban.service`
dir=`pwd`
service_file=${service_file//PatH/$dir}
echo $service_file >> /etc/systemd/system/ban.service
sudo systemctl daemon-reload
sudo systemctl enable test.service
sudo systemctl start test.service
