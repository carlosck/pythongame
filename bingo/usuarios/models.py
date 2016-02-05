from django.db import models

class Usuarios(models.Model):
	created = models.DateTimeField(auto_now_add=True)	
	name= models.CharField(max_length=100)
	lastname = models.CharField(max_length=100)
	username = models.CharField(max_length=100)
	password = models.TextField()
	



# Create your models here.
