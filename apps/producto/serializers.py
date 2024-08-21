from rest_framework import serializers

# from apps.user.serializers import UsuarioSerializer, UsuarioPresentacionSerializer
from .models import Producto


class ProductoSerializer(serializers.ModelSerializer):


	class Meta:

		model = Producto
		fields = ('pk_publica','Id_Sku', 'Titulo','Descripción','Disponibilidad', 'Precio', 'Moneda', 'Marca', 'Unidad_medida' )

	def __str__(self):

		return self.ProductoSerializer
	

class ProductoPublicSerializer(serializers.ModelSerializer):


	class Meta:

		model = Producto
		fields = ('pk_publica','Id_Sku', 'Titulo','Descripción','Disponibilidad', 'Imagen_QR', 'Precio', 'Moneda', 'Marca', 'Unidad_medida', 'Cantidad' )

	def __str__(self):

		return self.ProductoPublicSerializer


class ProductoprSerializer(serializers.ModelSerializer):

	# Imagen_QR = serializers.SerializerMethodField()
	class Meta:

		model = Producto
		fields = ('pk_publica','Id_Sku', 'Titulo','Descripción','Disponibilidad', 'Imagen_QR', 'Precio', 'Moneda', 'Marca', 'Unidad_medida' )

	def __str__(self):

		return self.ProductoprSerializer
	
	def get_Imagen_QR(self, obj):
		print(obj)
		return obj.Imagen_QR.url