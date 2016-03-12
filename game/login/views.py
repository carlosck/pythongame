from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ParseError
from rest_framework import status

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from login.serializers import UserSerializer
from login.serializers import UserProfileSerializer
from login.models import UserProfile
from pprint import pprint

class TestView(APIView):
	def get(self, request, format=None):
		return Response({'detail': "Hello Rest"})

	def post(self, request, format=None):
		try:
			data= request.data
			print("--->")
			print(data['user'])
			print("---|")
		except ParseError as error:
			return Response('Invalid JSON - {0}'.format(error.detail),
				status=status.HTTP_400_BAD_REQUEST
				)

		if "user" not in data or "password" not in data:
			return Response('Wrong fields',status=status.HTTP_401_UNAUTHORIZED)
		#
		#try:
			#user= User.objects.get(username=data['user'])
		#	user = authenticate(username='john', password='secret')
		#except user.DoesNotExist:
		#	return Response('no default user, please create one',status=status.HTTP_404_NOT_FOUND)
		user = authenticate(username=data['user'], password=data['password'])
		if user is not None:
			# the password verified for the user
			if user.is_active:
				token= Token.objects.get_or_create(user=user)
				return Response({'detail':'User is valid, active and authenticated','token':token[0].key,'error':False})
			else:
				return Response({'detail':'The password is valid, but the account has been disabled!','error':True})
		else:
			# the authentication system was unable to verify the username and password
			return Response({'detail':'The username and password were incorrect.','error':True})


		

		return Response({'detail':'post answer','token':token[0].key})
		
class AuthView(APIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	model = User
	serializer_class = UserProfileSerializer

	def get(self, request, format= None):
		return Response({'detail':'I suppose you are authenticated'})

	def post(self, request, format= None):
		print("--->")
		print("este")
		print("---|")
		# try
		# {
		# 	user_id= User.objects.get(username=data['user'])
		# 	user= User.objects.get(username=data['user'])
		# }
		user =UserProfile.objects.get(user=request.user)		
		pprint(user.user.id)
		#print(UserProfile.objects.get(username=request.user))
		#pprint.pprint(UserSerializer(request.user).data)
		return Response(UserProfileSerializer(user).data)

		#return Response({'detail':'I suppose you are authenticated'})	
# Create your views here.
