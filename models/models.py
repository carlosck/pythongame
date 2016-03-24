from core import db
from itsdangerous import (TimedJSONWebSignatureSerializer
						  as Serializer, BadSignature, SignatureExpired)
from flask import current_app

class User(db.Model):
	# def __init__(self, name, password, last_name, username, id, user_role,credit,active=True):
	# 	self.name = name
	# 	self.password = password
	# 	self.last_name = last_name
	# 	self.username = username
	# 	self.id = id
	# 	self.active = active
	# 	self.user_role = user_role
	# 	self.credit = credit
	__tablename__ = 'user'
	name= db.Column(db.String)
	passw= db.Column(db.String)
	last_name= db.Column(db.String)
	username= db.Column(db.String)
	id= db.Column(db.String,primary_key=True)
	active= db.Column(db.Boolean)
	user_role= db.Column(db.Integer)
	credit= db.Column(db.Integer)
	authenticated = db.Column(db.Boolean, default=False)
   
 
	def is_active(self):
		"""True, as all users are active."""
		return True

	def get_id(self):
		"""Return the email address to satisfy Flask-Login's requirements."""
		return self.username

	def is_authenticated(self):
		"""Return True if the user is authenticated."""
		return self.authenticated

	def is_anonymous(self):
		"""False, as anonymous users aren't supported."""
		return False
		
	def generate_auth_token(self,expiration = 600):
		print(current_app.config.get('SECRET_KEY'))
		s = Serializer(current_app.config.get('SECRET_KEY'), expires_in = expiration)
		return s.dumps({ 'id': self.id })
	
	@staticmethod
	def verify_auth_token(token):
		s = Serializer(current_app.config.get('SECRET_KEY'))
		try:
			data = s.loads(token)
		except SignatureExpired:
			return None # valid token, but expired
		except BadSignature:
			return None # invalid token
		user = User.query.get(data['id'])
		return user		