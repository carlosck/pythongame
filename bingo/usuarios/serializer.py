from rest_framework import serializers
from login.models import usuarios

class UsuariosSerializer(serializers.Serializer):
	pk = serializers.IntegerField(read_only= True)
	name= serializers.CharField(required= True,max_length=100)
	lastname= serializers.CharField(required= True,max_length=100)
	username= serializers.CharField(required= True,max_length=100)
	password= serializers.textField(required= True)

	def create(self, validated_data):
		return usuarios.objects.create(**validated_data)

	def update(self, instance, validated_data):
		instance.title= validated_data.get('title',instance.title)
		instance.name= validated_data.get('name',instance.name)
		instance.lastname= validated_data.get('lastname',instance.lastname)
		instance.username= validated_data.get('username',instance.username)
		instance.password= validated_data.get('password',instance.password)
		instance.save()
		return instance
