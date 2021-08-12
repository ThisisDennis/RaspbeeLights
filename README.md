# RaspbeeLights
## Descrition
This is a small minimalistic helper to control your zigbee devices via deConz Rest-API.
It was build to control my Lights via Rhasspy, the work isn't done yet.
This repository is a working example for the integration of the helper to rhasspy via "rhasspy-hermes-app"

You can use it without "Rhasspy-hermes-app" (https://github.com/rhasspy/rhasspy-hermes-app), you just need to build your own "intent-parser".

## Note
But i decided to publish it so that other people can benefit from the work done so far. Even if I don't find the time to continue working on it.
At the moment its only German, maybe some day i'll make it changeable.
## Requirements
python 3

# Setup
## Get an API-Key
I recommend to use https://www.postman.com/ or some alternative.. 
Go to your Phoscon-UI, under Setting/Gateway/Advanced there is a Button "Authenticate App", click it.
Now you have a few seconds to send {"devicetype": "your Application name"} via post to your phoscon-hostname e.g. 192.168.194:8080/api/
A better decription you can find here: https://dresden-elektronik.github.io/deconz-rest-doc/getting_started/

## Set up the helper
I will descripe the way this respository Example works.
In the file action-lights.py you will find a line "action-light conbee = lights.Light("yourConfigPath")" in our main-function. Just paste your config-path.
Fill your config-file like the config-example.

If you don't wanna have a service running the script in the background you might need to install some external libs-> in your path: pip3 install -r requirements.txt

If you wanna, just run sudo sh setup.sh. There are also logs.sh and reload.sh, these are just small simplifiers to show the logs or reload the service, if you change some code...
I hope there is nothing left.

# Usage
Structure:
action-light.py #handels mqtt-inputs and calls the parser
Rhasspy-hermes-app-parser.py #interprets the intents in the structure of rhasspy-hermes-app and passes it to the helper
RaspbeeLights.py #this helper handels the API-interaction

In the folder "language" you can find some example-sentences and slots to train you rhasspy instance. The slots must be the names of your light-groups, cause the script uses the api to read out what groups you have set up in phoscon.
I've added an untested python-script to print out the rooms for you (future task could be to print out a slot-file). You can also write a script to automatically add the groups to the rhasspy-slots and train.
If you change or add some light-groups, you need to change your slots in rhasspy and restart the script/pi/service what ever or you call the initRooms-function via voice command.

At this point the Script can only turn on, turn off and dimm groups.
There is a lot to do, but it's not difficult, you can easily expand the functionality. In most cases you can copy a function in RhasspyLights.py and change the payload.

Just take a look at the documentation: https://dresden-elektronik.github.io/deconz-rest-doc/getting_started/#get-a-list-of-all-lights
