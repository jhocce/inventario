from django.db import models
from apps.system.models import basemodel
from apps.user.models import user



class Producto(basemodel):
	
	Id_Sku =  models.CharField(max_length=100, default="")
	Titulo =  models.CharField(max_length=100, default="")
	Descripción =  models.CharField(max_length=500, default="", blank=True)
	Disponibilidad = models.BooleanField(default=False, blank=True)
	Precio = models.FloatField(blank=True, default=0.0)
	Tipos_moneda = (('USD','USD'), ('EUR','EUR'))
	Moneda = models.CharField(max_length=20, choices=Tipos_moneda, default='USD')
	Marca = models.CharField(max_length=100, default="", blank=True)
	Imagen_QR = models.ImageField(upload_to="imagenQR/", null=True, blank=True)
	Tipos_medida = (('pieza','pieza'), ('cajas','cajas'), ('kilos','kilos'), ('libras','libras'))
	Unidad_medida =  models.CharField(max_length=20, choices=Tipos_medida, default='pieza')
	Cantidad = models.IntegerField(default=0)
	creador = models.ForeignKey(user,
								related_name="creadorproducto", 
								null=True, 
								blank=True, 
								on_delete=models.CASCADE)
	
