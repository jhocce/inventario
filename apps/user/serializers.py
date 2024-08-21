from rest_framework import serializers
from apps.system.models import login

from .models import user


class UsuarioPresentacionSerializer(serializers.ModelSerializer):


	class Meta:

		model = user
		fields = ('pk_publica', 'username','email',"Tipo", 'Nombres', 'Apellidos', "Contacto" ) 

	def __str__(self):

		return self.UsuarioPresentacionSerializer




class UsuarioSerializer(serializers.ModelSerializer):


	class Meta:

		model = user
		fields = ('pk_publica','username','email',"Tipo", 'Nombres', 'Apellidos', 'password', "Contacto","Comentarios" ) 

	def __str__(self):

		return self.UsuarioSerializer

class LoginSerializer(serializers.ModelSerializer):

	class Meta:

		model = login
		fields = ('email', 'password') 

	def __str__(self):

		return self.LoginSerializer
	

