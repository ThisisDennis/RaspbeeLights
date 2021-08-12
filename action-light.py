import lib.Rhasspy_Hermes_App_Parser as lights
from rhasspyhermes.nlu import NluIntent
from rhasspyhermes_app import EndSession, HermesApp

conbee = None
app = HermesApp("LightApp")

@app.on_intent("RaspbeeLight:TurnOn")
async def turnOnGroup(intent: NluIntent):
    """Lights Groupt On"""
    answer = conbee.turnOnGroup(intent)
    return EndSession(answer)

@app.on_intent("RaspbeeLight:TurnOff")
async def turnOffGroup(intent: NluIntent):
    """Lights Groupt Off"""
    answer = conbee.turnOffGroup(intent)
    return EndSession(answer)

@app.on_intent("RaspbeeLight:TurnRoomOn")
async def turnOnRoom(intent: NluIntent):
    """Lights Room On"""
    answer = conbee.turnOnRoom(intent)
    return EndSession(answer)

@app.on_intent("RaspbeeLight:TurnRoomOff")
async def turnOffRoom(intent: NluIntent):
    """Lights Room Off"""
    answer = conbee.turnOffRoom(intent)
    return EndSession(answer)

@app.on_intent("RaspbeeLight:Dimm")
async def dimmGroup(intent: NluIntent):
    """Dimm Lights"""
    answer = conbee.dimmGroup(intent)
    return EndSession(answer)

if __name__ == "__main__":
    conbee = lights.Light("yourConfigPath")
    app.run()
