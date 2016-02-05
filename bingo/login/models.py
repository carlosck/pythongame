from django.db import models
from django import forms

from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight
# Create your models here.

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0],item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item)for item in get_all_styles())




class User(models.Model):

	def __str__(self):
		return self.name
		
	id = models.AutoField(primary_key=True)
	user  = models.CharField(max_length=15)
	name  = models.CharField(max_length=100)
	password = forms.CharField(widget=forms.PasswordInput)

