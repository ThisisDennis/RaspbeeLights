#!/bin/bash
sudo systemctl stop rhasspy.skill.light.service
sudo systemctl daemon-reload
sudo systemctl start rhasspy.skill.light.service