import io
import requests
import configparser
import json

class RaspbeeLights(object):

    CONFIGURATION_ENCODING_FORMAT = "utf-8"
    CONFIG_INI = "config.ini"

    payload = {}
    baseAPI = ""
    rooms = {}

    def __init__(self, configPath):
        self.CONFIG_INI = configPath
        conf = self.read_configuration_file(self.CONFIG_INI)
        self.baseAPI = self.buildBaseAPI(conf)
        self.initRooms()

    class ConfigParser(configparser.ConfigParser):
        def to_dict(self):
            return {section : {option_name : option for option_name, option in self.items(section)} for section in self.sections()}

    def read_configuration_file(self, configuration_file):
        try:
            with io.open(configuration_file, encoding=self.CONFIGURATION_ENCODING_FORMAT) as f:
                conf_parser = self.ConfigParser()
                conf_parser.read_file(f)
                return conf_parser.to_dict()
        except (IOError, configparser.Error) as e:
            return dict()

    def buildBaseAPI(self, conf):
        return  conf['setup']['host'] + ':' + conf['setup']['port'] + '/api/' + conf['secret']['api_key']

    def readLightSetting(self):
        res = requests.get(self.baseAPI + "/groups/")
        if res.status_code == 200:
            return json.loads(res.text)
        else:
            return None

    def initRooms(self):
        lightSetup = self.readLightSetting()
        self.rooms = {}
        for key in lightSetup:
            if lightSetup[key]['type'] == 'LightGroup':
                self.rooms[lightSetup[key]['name'].upper()] = lightSetup[key]['id']
    
    def getLightSetup(self):
        return self.readLightSetting()

    def getRooms(self):
        return self.rooms
        
    def turnOnGroup(self, groupName):
        payload = {"on":True}
        try:
            groupID = self.rooms[groupName.upper()]
            out = requests.put(self.baseAPI + "/groups/" + groupID + "/action/", json=payload)
            return "Habe Lichter in " + groupName + " angeschaltet"
        except:
            return self.noLightsException(groupName)

    def turnOffGroup(self, groupName):
        payload = {"on":False}
        try:
            groupID = self.rooms[groupName.upper()]
            out = requests.put(self.baseAPI + "/groups/" + groupID + "/action/", json=payload)
            return "Habe Lichter in " + groupName + " ausgeschaltet"
        except:
            return self.noLightsException(groupName)

    def dimmGroup(self, groupName, percent):
        bri = 2.55 * int(percent[0])
        bri = int(bri)
        if percent[0] < 5:
            payload = {"on":False}
        else:
            payload = {"on":True ,"bri":bri}
        try:
            groupID = self.rooms[groupName.upper()]
            out = requests.put(self.baseAPI + "/groups/" + groupID + "/action/", json=payload)
            return "Habe Lichter in " + groupName + " auf " + percent[1] + " Prozent gedimmt"
        except:
            return self.noLightsException(groupName)
    
    def noLightsException(self, groupName):
        if len(groupName)>0:
            return "Finde keine Lichter in " + groupName
        else:
            return u"Ich weiß leider nicht, um welche Lichter es sich handelt."