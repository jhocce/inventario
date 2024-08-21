from rest_framework import serializers

from apps.user.serializers import UsuarioPresentacionSerializer
from apps.producto.serializers import ProductoprSerializer
from .models import retiro, deposito


class retiroSerializer(serializers.ModelSerializer):
	
	retira = UsuarioPresentacionSerializer(many=False, read_only=True)
	producto = ProductoprSerializer(many=False, read_only=True)
	class Meta:

		model = retiro
		fields = ('pk_publica','retira', 'producto','cantidad')

	def __str__(self):

		return self.retiroSerializer


class depositoSerializer(serializers.ModelSerializer):
	
	deposita = UsuarioPresentacionSerializer(many=False, read_only=True)
	producto = ProductoprSerializer(many=False, read_only=True)

	class Meta:

		model = deposito
		fields = ('pk_publica','deposita', 'producto','cantidad')

	def __str__(self):

		return self.depositoSerializer
	