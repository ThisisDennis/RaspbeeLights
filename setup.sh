#!/bin/bash

#pip3 install python-vlc
#pip3 install -r requirements.txt


# Absolute path to this script, e.g. /home/user/bin/foo.sh
SCRIPT=$(readlink -f "$0")
# Absolute path this script is in, thus /home/user/bin
SCRIPTPATH=$(dirname "$SCRIPT")
echo $SCRIPTPATH

sudo rm -f /lib/systemd/system/rhasspy.skill.light.service
touch /lib/systemd/system/rhasspy.skill.light.service
:> /lib/systemd/system/rhasspy.skill.light.service

echo "
[Unit]
Description=Rhasspy Light Skill
After=multi-user.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 $SCRIPTPATH/action-light.py
Restart=on-abort

[Install]
WantedBy=multi-user.target

  " >>  /lib/systemd/system/rhasspy.skill.light.service


chmod +x action-light.py


sudo sudo chmod 644 /lib/systemd/system/rhasspy.skill.light.service
sudo systemctl stop rhasspy.skill.light.service
sudo systemctl daemon-reload
sudo systemctl enable rhasspy.skill.light.service
sudo systemctl start rhasspy.skill.light.service
#sudo reboot
