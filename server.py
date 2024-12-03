import socketio
from flask import Flask

app = Flask(__name__)
sio = socketio.Server()
app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)

player_list = []


class Player:
    def __init__(self,x,y,id,name):
        self.x:int = x
        self.y:int = y
        self.id = id
        self.name:str = name
        self.velocity = 10
        self.animationFrame = 0
        self.flip = False

    def to_dict(self):
        return {
            "x": self.x,
            "y": self.y,
            "id": self.id,
            "name": self.name,
            "velocity": self.velocity,
            "animationFrame": self.animationFrame,
            'flip': self.flip
        }
# Obsługa nowego połączenia
@sio.event
def connect(sid,environ):
    print(f'Gracz {sid} połączony')
    sio.emit('message', {'text': 'Witamy w grze!'}, room=sid)

# Obsługa ruchu gracza
@sio.event
def player_move(sid, data):
    global player_list
    for Player in player_list:
        if Player.id == sid:
            if data == 'W':
                Player.y -= Player.velocity
            elif data == 'S':
                Player.y += Player.velocity
            elif data == 'A':
                Player.x -= Player.velocity
            elif data == 'D':
                Player.x += Player.velocity
            sio.emit('player_moved', [Player.x,Player.y])
        
            

# Obsługa rozłączenia
@sio.event
def disconnect(sid):
    print(f'Gracz {sid} rozłączony')
    global player_list 
    player_list = [Player for Player in player_list if Player.id != sid]
    print(len(player_list))

@sio.event
def addPlayer(sid,name):
    global player_list 
    newPlayer = Player(0,0,sid,name)
    player_list.append(newPlayer)
    print(len(player_list)) 

@sio.event
def requestPlayerData(sid):
    global player_list
    players_data = [player.to_dict() for player in player_list]
    sio.emit('returnPlayerData', players_data)

@sio.event
def changeFrame(sid,data):
    global player_list
    for Player in player_list:
        if Player.id == sid:
            Player.animationFrame = data[0]
            Player.flip = data[1]

@sio.event
def addObject(sid,data):
    sio.emit('newObject', data)

if __name__ == '__main__':
    app.run(port=5000)
