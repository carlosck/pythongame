from login.models import Snippet
from login.serializers import SnippetSerializer
from login.serializers import UserSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework import permissions
from django.http import HttpResponse

from rest_framework import authentication
from rest_framework import exceptions

class SnippetList(generics.ListCreateAPIView):
	queryset= Snippet.objects.all()
	serializer_class = SnippetSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
	def perform_create(self, serializer):
		serializer.save(owner= self.request.user)		
				

class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Snippet.objects.all()
	serializer_class= SnippetSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
		

class UserList(generics.ListAPIView):
	queryset= User.objects.all()
	serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
	queryset = User.objects.all()
	serializer_class= UserSerializer

# Create your views here.
class BingoLogin(authentication.BaseAuthentication):
	def authentication(self, request):
		username= request.Meta.get('X_USERNAME')
		if not username:
			return None

		try:
			user= User.objects.get(username=username)
		except user.DoesNotExist:
			raise exceptions.AuthenticationFailed('No such user')
		return (user,None)			

def index(request):
	return HttpResponse("Hello, world")