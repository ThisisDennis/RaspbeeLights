from rhasspyhermes.nlu import NluIntent
from .RaspbeeLights import RaspbeeLights as lights
import os

class Light(object):
    ligthsObject = None
    '''
    Parse intent and execute the right function
    '''
    def __init__(self, config = "/home/pi/skills-server/skills/raspeeLight/config.ini"): 
        self.ligthsObject = lights(config)

    def getSiteID(self, intent):
        return intent.site_id
    
    def getGroup(self, intent):
        for slot in intent.slots:
            if slot.slot_name == 'group':
                return slot.raw_value
        return None
    
    def getPercent(self, intent):
        for slot in intent.slots:
            if slot.slot_name == 'percent':
                return [slot.value['value'], slot.raw_value]
        return None

    def turnOnGroup(self, intent):
        group = self.getGroup(intent)
        return self.ligthsObject.turnOnGroup(group)
    
    def turnOffGroup(self, intent):
        group = self.getGroup(intent)
        return self.ligthsObject.turnOffGroup(group)

    def turnOffRoom(self, intent):
        room = self.getSiteID(intent)
        return self.ligthsObject.turnOffGroup(room)

    def turnOnRoom(self, intent):
        room = self.getSiteID(intent)
        return self.ligthsObject.turnOnGroup(room)

    def dimmGroup(self, intent):
        group   = self.getGroup(intent)
        percent = self.getPercent(intent)
        return self.ligthsObject.dimmGroup(group, percent)
    
    