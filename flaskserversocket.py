async_mode = None

if async_mode is None:
	try:
		import eventlet
		async_mode = 'eventlet'
	except ImportError:
		pass

	if async_mode is None:
		try:
			from gevent import monkey
			async_mode = 'gevent'
		except ImportError:
			pass

	if async_mode is None:
		async_mode = 'threading'

	print('async_mode is ' + async_mode)

# monkey patching is necessary because this application uses a background
# thread
if async_mode == 'eventlet':
	import eventlet
	eventlet.monkey_patch()
elif async_mode == 'gevent':
	from gevent import monkey
	monkey.patch_all()

import time
from threading import Thread
from flask import Flask, render_template, session, request, flash
from flask_socketio import SocketIO, emit, join_room, leave_room, \
	close_room, rooms, disconnect

from flask_login import current_user
from flask.ext.login import LoginManager,login_user , logout_user , current_user , login_required
from pprint import pprint
import functools
from flask.ext.bcrypt import Bcrypt
from hashlib import md5

from models.models import User
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
import json
#import MySQLdb
#from flask.ext.sqlalchemy import SQLAlchemy
from core import db

#todo: make an object
users = {}

BINGO 	  = {'name':'BINGO','value':0,'playerToStart':2}
BLACKJACK = {'name':'BLACKJACK','value':1,'playerToStart':2}
LOTERIA   = {'name':'LOTERIA','value':2,'playerToStart':2}

games = [BINGO,BLACKJACK,LOTERIA]

BINGO_ROOMS={'1':{'name':'BINGO_1','players':{}}}
BLACK_ROOMS=['BLACK_1']
LOTERIA_ROOMS=['LOTERIA_1']
gameRooms={'BINGO':BINGO_ROOMS,'BLACKJACK':BLACK_ROOMS,"LOTERIA":LOTERIA_ROOMS}


numUsers = 0
NumPlayersToStartGame = 2

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
serializer = Serializer(app.config['SECRET_KEY'])
login_manager = LoginManager()
login_manager.init_app(app)
#socketio = SocketIO(app, async_mode=async_mode)
socketio = SocketIO(app)
thread = None


#db = MySQLdb.connect(host="localhost", user="root", passwd="", db="test")

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/bingo?unix_socket=/Applications/MAMP/tmp/mysql/mysql.sock'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql:///bingo?unix_socket=/Applications/MAMP/tmp/mysql/mysql.sock'
#db = SQLAlchemy(app)
db.init_app(app)
bcrypt = Bcrypt(app)
#cur = db.cursor()


def background_thread():
	"""Example of how to send server generated events to clients."""
	count = 0
	while True:
		time.sleep(10)
		count += 1
		socketio.emit('my response',
					  {'data': 'Server generated event', 'count': count},
					  namespace='/')


@app.route('/')
def index():
	global thread
	
	print("index.htmls")    
	return render_template('index.html')

@app.route('/delete')
def delete():

	global numUsers
	numUsers = 0
	# if thread is None:
	# 	thread = Thread(target=background_thread)
	# 	thread.daemon = True
	# 	thread.start()
	
	print("delete") 	   
	#return render_template('index.html')

@app.route('/login',methods=['GET','POST'])
def login():			
	if request.method == 'GET':
	    return render_template('login.html')
	
	if 'username' in session:
		return ("{'error':False}")

	error = None
	
	if request.method == 'POST':
		username = request.form['user']
		password = request.form['password']				
		user = User.query.filter_by(username=username).first()

		if user:						
			if bcrypt.check_password_hash(user.passw, password):				
				user.authenticated = True
				db.session.add(user)
				db.session.commit()
				login_user(user, remember=True)				
				token = user.generate_auth_token()
				users[token.decode('ascii')]= username							
				cadena = { 'error' : False,'credit': str(user.credit),'token':token.decode('ascii'),'username': user.username}				
				return (json.dumps(cadena))
		else:
			return ({'error':True,'data':'login error'});	
				
def hash_pass(password):
    """
    Return the md5 hash of the password+salt
    """
    salted_password = password + app.secret_key
    return md5.new(salted_password).hexdigest()

def logout():
    """Logout the current user."""
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()

@app.route('/start')
def start():
	socketio.emit('start game', {'data': 'game', 'total': numUsers},broadcast=True)
		

# @socketio.on('connect')
# def connect_handler():
# 	print("connect")
# 	global numUsers
# 	numUsers=numUsers+1
# 	print("----------->")
# 	#pprint(token)
# 	print("----------->")
# 	if current_user.is_authenticated:
# 		checkNumPLayers()
# 		getGameTypes()
# 		emit('my response',
# 			 {'message': '{0} has joined'.format(current_user.name)},
# 			 broadcast=True)
# 	else:
# 		socketio.emit('response error', {'data': 'game', 'total': 'no auth'})
		#return False  # not allowed here

@socketio.on('set token', namespace='/')
def set_token(data):	
	#print(users[se]["username"])	
	print(request.sid)
	session['api_session_token'] = data["token"]
	getGameTypes()

	#session['receive_count'] = session.get('receive_count', 0) + 1
	#emit('my response',{'data': message['data'], 'count': session['receive_count']})
@socketio.on('connect')
def test_connect():
    print("request.sid--->")
    print(request.sid)
# @socketio.on('connect', namespace='/')
# def test_connect():	
	#print(session.get('receive_count', 0))
	#emit('you connect', {'data': 'Connected', 'total': numUsers})
	
def authenticated_only(f):
	@functools.wraps(f)
	def wrapped(*args, **kwargs):
		if not current_user.is_authenticated:
			disconnect()
		else:
			return f(*args, **kwargs)
	return wrapped

@socketio.on('my event', namespace='/')
def test_message(message):
	print("message -->")
	print(message)
	session['receive_count'] = session.get('receive_count', 0) + 1
	emit('my response',
		 {'data': message['data'], 'count': session['receive_count']})

@socketio.on('send', namespace='/')
def send(message):
	print("send")
	session['receive_count'] = session.get('receive_count', 0) + 1
	emit('my response',
		 {'data': message['data'], 'count': session['receive_count']})

@socketio.on('my broadcast event', namespace='/')
def test_broadcast_message(message):
	print("broadcast")
	pprint(message)
	pprint(session.get('receive_count', 0) )
	session['receive_count'] = session.get('receive_count', 0) + 1
	emit('broadcast',
		 {'data': message['data'], 'count': session['receive_count']},
		 broadcast=True)


@socketio.on('join', namespace='/')
def join(message):
	print("join")
	join_room(message['room'])
	session['receive_count'] = session.get('receive_count', 0) + 1
	emit('my response',
		 {'data': 'In rooms: ' + ', '.join(rooms()),
		  'count': session['receive_count']})


@socketio.on('leave', namespace='/')
def leave(message):
	print("leave")
	leave_room(message['room'])
	session['receive_count'] = session.get('receive_count', 0) + 1
	emit('my response',
		 {'data': 'In rooms: ' + ', '.join(rooms()),
		  'count': session['receive_count']})


@socketio.on('close room', namespace='/test')
def close(message):
	print("close")
	session['receive_count'] = session.get('receive_count', 0) + 1
	emit('my response', {'data': 'Room ' + message['room'] + ' is closing.',
						 'count': session['receive_count']},
		 room=message['room'])
	close_room(message['room'])


@socketio.on('my room event', namespace='/')
def send_room_message(message):
	print("my room event")
	session['receive_count'] = session.get('receive_count', 0) + 1
	emit('my response',
		 {'data': message['data'], 'count': session['receive_count']},
		 room=message['room'])


@socketio.on('disconnect request', namespace='/')
def disconnect_request():
	session['receive_count'] = session.get('receive_count', 0) + 1
	print("disconnect request")	
	emit('my response',
		 {'data': 'Disconnected!', 'count': session['receive_count']})
	disconnect()



@socketio.on('disconnect', namespace='/')
def test_disconnect():
	global numUsers
	print("disconnect")	
	numUsers=numUsers-1
	print('Client disconnected', request.sid)

@socketio.on_error_default  # handles all namespaces without an explicit error handler
def default_error_handler(e):
	print("default_error_handler")
	pprint(e)

@socketio.on('gametype', namespace='/')
def gametype(data):
	#Todo:validations if data[type]< games.length
	print("changing to  -->")
	token =data["token"]	
	username = users[token]	
	
	#from 0 to BINGO
	gameTypeValue = data["type"]
	print("gameTypeValue="+str(gameTypeValue))
	gameType= games[gameTypeValue]["name"]
	
	#get available room from bingo "BINGO_1"
	#Todo: change harcoded "1" to var available_room
	playersInRoom= getPlayersInRoom(gameType)
	gameTypeRoom = str(gameRooms[gameType]["1"]["name"])	
	playersInRoom[token]= username	
	
	join_room(gameTypeRoom)

	player_list= []
	for tok, usern in playersInRoom.iteritems():
		print(usern)
		player_list.append(usern)
	
	# print("->>>>>")
	# for room in rooms():
	# 	pprint(room)
	# print("<<<<-")
	
	socketio.send('join room', {'data': gameTypeRoom, 'gametype':gameType, 'players': player_list},room=gameTypeRoom)
	
	checkNumPlayers(gameTypeValue,gameType,gameTypeRoom)

def checkNumPlayers(gameTypeValue,gameType,gameTypeRoom):
	print("<checkNumPlayers>")
	numPlayersTostart =games[gameTypeValue]["playerToStart"]
	print(numPlayersTostart)
	players= getNumPlayersInRoom(gameType)
	socketio.emit('user connect', {'data': 'numUsers', 'total': numPlayersTostart,'users' : players},room=gameTypeRoom)
	if players == numPlayersTostart:
		initGame(gameTypeRoom,gameType)

def initGame(gameTypeRoom,gameType):
	print("<initGame>")
	items='';

	if(gametype is 'BINGO'):
	
		for i in range(15):
			items[i]=random.randint(1, 15)
	
	socketio.emit('init game', {'game': gameType,'room':gameTypeRoom,'items':items})

def getGameTypes():			
	socketio.emit('list rooms', {'data': 'game', 'rooms': games})

def getPlayersInRoom(gameTypeValue):	
	return gameRooms[gameTypeValue]["1"]["players"]

def getNumPlayersInRoom(gameTypeValue):	
	return len(gameRooms[gameTypeValue]["1"]["players"])

@login_manager.user_loader
def user_loader(user_id):
	"""Given *user_id*, return the associated User object.

	:param unicode user_id: user_id (email) user to retrieve
	"""
	return User.query.get(user_id)

def load_user(user_id):
    return User.get(user_id)

if __name__ == '__main__':
	socketio.run(app, host='192.168.1.171',debug=True)

