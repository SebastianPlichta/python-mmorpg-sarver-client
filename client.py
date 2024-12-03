import socketio
import magicAttack

sio = socketio.Client()
globalName:str
globalPlayerList = {}
globalObjectList = []
globalEnemiesList = []

@sio.event
def connect():
    print('Połączono z serwerem')
    
@sio.event
def message(data):
    print('Wiadomość od serwera:', data['text'])

@sio.event
def player_moved(data):
    pass

@sio.event
def disconnect():
    global globalName

# Wysyłanie ruchu gracza do serwera
def move_player(direction:int):
    sio.emit('player_move', direction)

def PlayerData():
    sio.emit('requestPlayerData')

@sio.event
def returnPlayerData(player_list):
    global globalPlayerList
    globalPlayerList = player_list

@sio.event
def newObject(data):
    if data[0] == 1:
        globalObjectList.append(magicAttack.MagicAttack(data[1], data[2][0],data[2][1], data[3]))

def CtS(name):
    global globalName 
    globalName = name
    sio.connect('http://localhost:5000')
    sio.emit('addPlayer', name)

def changeFrame(data):
    sio.emit('changeFrame', data)

def addObject(data):
    sio.emit('addObject', data)

def removeFromList(obj):
    globalObjectList.remove(obj)