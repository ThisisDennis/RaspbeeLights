import io
import requests
import configparser
import json
import time

class RaspbeeLights(object):

    CONFIGURATION_ENCODING_FORMAT = "utf-8"
    CONFIG_INI = "config.ini"

    payload = {}
    baseAPI = ""
    rooms = {}
    '''
    Try to Connect your deConz/Phoscon/Conbee API
    via Put
    '''
    def saveRequestPut(self, url, payload):
        try:
            output = requests.put(url, json = payload)
            return output
        except Exception as e:
            print("Got an error:")
            print(e)
            print("Connection refused by the server..")
            print("Let me sleep for 5 seconds")
            print("ZZzzzz...")
            time.sleep(5)
            print("Was a nice sleep, now let me continue...")
            return -1
    '''
    Try to Connect your deConz/Phoscon/Conbee API
    via Get
    '''
    def saveRequestGet(self, url):
        try:
            output = requests.get(url)
            print(output)
            return output
        except:
            print("Connection refused by the server..")
            print("Let me sleep for 5 seconds")
            print("ZZzzzz...")
            time.sleep(5)
            print("Was a nice sleep, now let me continue...")
            return -1

    def __init__(self, configPath):
        self.CONFIG_INI = configPath
        conf = self.read_configuration_file(self.CONFIG_INI)
        self.baseAPI = self.buildBaseAPI(conf)
        self.initRooms()
    '''
    Parse the config Data
    '''
    class ConfigParser(configparser.ConfigParser):
        def to_dict(self):
            return {section : {option_name : option for option_name, option in self.items(section)} for section in self.sections()}
    '''
    Read the Config-File to get your API-Key, Hostname and Port
    '''
    def read_configuration_file(self, configuration_file):
        try:
            with io.open(configuration_file, encoding=self.CONFIGURATION_ENCODING_FORMAT) as f:
                conf_parser = self.ConfigParser()
                conf_parser.read_file(f)
                return conf_parser.to_dict()
        except (IOError, configparser.Error) as e:
            return dict()
    '''
    Let's make our lives easier and build a api-base-path like
    198.168.178.19:80/api/BE23234B
    '''
    def buildBaseAPI(self, conf):
        return  conf['setup']['host'] + ':' + conf['setup']['port'] + '/api/' + conf['secret']['api_key']

    '''
    Read light-information,
    198.168.178.19:80/api/BE23234B
    you can easily check this out by adding your api-base-path + /groups/ into the browser or Postman.
    example:
    198.168.178.19:80/api/BE23234B/groups/
    '''
    def readLightSetting(self):
        res = self.saveRequestGet(self.baseAPI + "/groups/")
        if res.status_code == 200:
            return json.loads(res.text)
        else:
            return None
    '''
    read light-informations and map the name to the light-id,
    so we can match our spoken input to the light-ID
    every time you change the light you just need to restart or call RaspbeeLights.initRooms()
    '''
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
            self.saveRequestPut(self.baseAPI + "/groups/" + groupID + "/action/", payload)
            return "Habe Lichter in " + groupName + " angeschaltet"
        except Exception as e:
            print(e.message)
            return self.noLightsException(groupName, e)

    def turnOffGroup(self, groupName):
        payload = {"on":False}
        try:
            groupID = self.rooms[groupName.upper()]
            self.saveRequestPut(self.baseAPI + "/groups/" + groupID + "/action/", payload)
            return "Habe Lichter in " + groupName + " ausgeschaltet"
        except Exception as e:
            print(e.message)
            return self.noLightsException(groupName, e)
    '''
    calculate percent to bri and dimm the group
    '''
    def dimmGroup(self, groupName, percent):
        bri = 2.55 * int(percent[0])
        bri = int(bri)
        if percent[0] < 5:
            payload = {"on":False}
        else:
            payload = {"on":True ,"bri":bri}
        try:
            groupID = self.rooms[groupName.upper()]
            self.saveRequestPut(self.baseAPI + "/groups/" + groupID + "/action/", payload)
            return "Habe Lichter in " + groupName + " auf " + percent[1] + " Prozent gedimmt"
        except Exception as e:
            print(e.message)
            return self.noLightsException(groupName,e)
    '''
    If there are no lights, we need an anwser
    '''
    def noLightsException(self, groupName, e=0):

        if len(groupName)>0:
            return "Finde keine Lichter in " + groupName
        else:
            return u"Ich weiß leider nicht, um welche Lichter es sich handelt."