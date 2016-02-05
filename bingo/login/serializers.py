from rest_framework import serializers
from login.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES

from django.contrib.auth.models import User

class SnippetSerializer(serializers.Serializer):
	class Meta:
		model = Snippet
		fields= ('id','title','code','linenos','language','style','owner')
		owner = serializers.ReadOnlyField(source='owner.username')


	def create(self, validated_data):
		"""
		create and return a new 'Snippet' instance, given the validated data.
		"""
		return Snippet.objects.create(**validated_data)
	
	def update(self, instance, validated_data):
		instance.title= validated_data.get('title',instance.title)
		instance.code= validated_data.get('code',instance.code)
		instance.linenos= validated_data.get('linenos',instance.linenos)
		instance.style= validated_data.get('style',instance.style)
		instance.save()
		return instance

class UserSerializer(serializers.ModelSerializer):
	snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())

	class Meta:
		model  = User
		fields = ('id','username','snippets')		