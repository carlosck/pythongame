from rest_framework import serializers
from login.models import UserProfile

class UserSerializer(serializers.Serializer):
	id = serializers.CharField()
	username = serializers.CharField()
	first_name = serializers.CharField()
	last_name = serializers.CharField()
	email = serializers.CharField()

	def create(self, validated_data):
		return User.objects.create(**validated_data)
class UserProfileSerializer(serializers.Serializer):
	# class Meta:
	# 	model  =UserProfile
	# 	fields = ('id','credit','name')
	# 	depth  = 1
	pk = serializers.IntegerField(read_only=True)	
	credit = serializers.CharField()
	user = UserSerializer()
	
	#username = serializers.CharField()

	def create(self, validated_data):
		return User.objects.create(**validated_data)

		



