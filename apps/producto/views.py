from django.shortcuts import render
import qrcode
import os
import time
import string
import secrets
import threading

from datetime import datetime
# Create your views here.
from django.db.models import Q, F
from ast import literal_eval
from django.http import Http404
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.system.monitor import MonitorMixin
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from django.core.paginator import Paginator

from .serializers import ProductoSerializer, ProductoPublicSerializer, ProductoprSerializer
from .models import Producto
from django.core.files import File
from django.conf import settings
from django.core.files.uploadedfile import UploadedFile

class ProductoAPI(MonitorMixin,CreateAPIView, ListAPIView, 
	RetrieveAPIView, UpdateAPIView, DestroyAPIView, APIView):
	
	serializer_class = ProductoSerializer
	model = Producto
	
	def update(self, request, *arg, **kwargs):
		"""Enviar por get el "pk" del producto el cual se actualizaran los datos"""
		try:
			if self.pk_publica is None:
				self.MensajeListAdd(mensaje_user='Ocurrieron errores al momento de guardar el Producto',
				mensaje_server='No se a enviado correctamente la variable "pk" correspondiente al objeto a actualizar en la URL', status='error')
				return Response(self.salida(), status=400)
			else:
				try:
					print(self.get_user())
					
					objeto = self.model.objects.get(pk_publica=self.pk_publica, 
						Status=True )
				except self.model.DoesNotExist:
					self.MensajeListAdd(mensaje_user = 'Ocurrieron uno o mas errores a actualizar el Producto',
						mensaje_server = 'El objeto no existe o no pertenece al usuario al que esta relacionado al token')
					return Response(self.salida(), status=404)
				
				serviciosSerializer = self.serializer_class( objeto, data= request.data, partial=True)
				if serviciosSerializer.is_valid():
				
					serviciosSerializer.save()
					self.MensajeListAdd(mensaje_user='El Producto a sido guardado con exito', status='success')
					self.JsonAdd(json = serviciosSerializer.data )
					return Response( self.salida(), status=200)
				else:
					self.JsonAdd(json = serviciosSerializer.errors )
					self.MensajeListAdd(mensaje_user='Ocurrieron errores al momento de guardar El Producto',
						mensaje_server=serviciosSerializer.errors, status='error')

					return Response(self.salida(), status=200)
		except Exception as e:
			self.MensajeListAdd(mensaje_server  = str(e))
			return Response(self.salida(), status=500)
		
	def post(self, request, *arg, **kwargs):
	    
		try:
			serviciosSerializer = self.serializer_class(data= request.data)
			if serviciosSerializer.is_valid():
				
				
				try:
					while True:
						alphabet = string.ascii_letters + string.digits
						code = ''.join(secrets.choice(alphabet) for i in range(15))
						Producto.objects.get(Codigo=code)
				except Exception as e:
					pass
				qr = {
					"code":code
				}
				img = qrcode.make(qr)
				url = settings.MEDIA_ROOT_TEMP + "\{0}.png".format(code)
				f = open(url , "wb")
				img.save(f)
				f.close()
				serviciosSerializer.validated_data['Codigo'] = code
				serviciosSerializer.validated_data['creador'] = self.get_user()
				serviciosSerializer.save()
				reopen = open(url, "rb")
				django_file = File(reopen)
				
				serviciosSerializer.instance.Imagen_QR.save("QR.png",django_file, save=True)
				serviciosSerializer.instance.save()
				reopen.close()
				os.remove(url)

				
				self.MensajeListAdd(mensaje_user='Producto Guardado Exitosamente', status='success')
	
				data = serviciosSerializer.data
				data['Imagen_QR'] = serviciosSerializer.instance.Imagen_QR.url
				self.JsonAdd(json=dict(data))			
				return Response(self.salida(), status=200)

			else:
				self.JsonAdd(json = serviciosSerializer.errors )
				self.MensajeListAdd(mensaje_user='Ocurrieron errores al momento de guardar el Producto',
					mensaje_server=serviciosSerializer.errors, status='error')
				return Response(self.salida(), status=200)

		except Exception as e:
			self.MensajeListAdd(mensaje_user='Ocurrieron errores al momento de guardar el Producto', mensaje_server  = str(e))
			return Response(self.salida(), status=500)
		
	def get(self, request, *arg, **kwargs):
		""" Enviar por get "pk" con la clave primaria del registro a buscar, el no enviar este valor implica la obtencion
		 de todos los registros en cuestion de ser asi enviar: \n
		    count: numero de elmentos por pagina \n
		    page: numero de pagina \n
		    Para el caso de obtener el producto a traves del codigo QR enviar solo \n
		    code: codigo escaneado \n
			
			"""
		try:
			code_qr = request.GET.get('code')
			if code_qr != None:
				query =  self.model.objects.get(Status=True, Codigo=code_qr)
				if query is None:
					self.MensajeListAdd(mensaje_user = 'El Producto no existe',
						mensaje_server = 'El Producto no existe o no pertenece al usuario relacionado con el token o el pk')			
					return Response(self.salida(), status=200)
				else:
					f = ProductoPublicSerializer(query)
					self.JsonAdd(json=f.data)			
					return Response(self.salida(), status=200)
			usuario = self.get_user()	
			if self.pk_publica is None:

				query =  self.model.objects.filter(Status=True)
				total_count = query.count()
				if self.count and self.page:
					paginacion= Paginator(query,self.count)
					
					if len(paginacion.page(1)) == 0:
						
						pass
					else:
						query= paginacion.page(self.page)
				if query is not None and total_count!=0:
					
					total_count = query.object_list.count()
					f = ProductoPublicSerializer(query, many=True)
					self.JsonAdd(json={
						"total_count":total_count,
						"data":f.data
						})
				else:
					self.JsonAdd(json={
						"total_count":0,
						"data":[]
						})
					self.MensajeListAdd(mensaje_user = 'No hay registros')
				return Response(self.salida(), status=200)
			else:
				# query = self.get_object()
				if usuario.Tipo == "Admin" or usuario.Tipo == "super":
					# query =  self.model.objects.filter(Q(tipo=self.usuario)&Q(Status=True))
					query =  self.model.objects.get(Status=True, pk_publica=self.pk_publica)
				elif usuario.Tipo == "Coordinador":
					# self.MensajeListAdd( mensaje_user = 'No autorizado',
					# 		mensaje_server="No autorizado",
					# 		status= 303)
					# return Response(self.salida(), status=303)
					
					query =  self.model.objects.get(Status=True, pk_publica=self.pk_publica)
				if query is None:
					self.MensajeListAdd(mensaje_user = 'El Producto no existe',
						mensaje_server = 'El Producto no existe o no pertenece al usuario relacionado con el token o el pk')			
					return Response(self.salida(), status=200)
				else:
					f = ProductoPublicSerializer(query)
					self.JsonAdd(json=f.data)			
					return Response(self.salida(), status=200)

		except Exception as e:
			self.MensajeListAdd(mensaje_server  = str(e))
			return Response(self.salida(), status=500)

	def delete(self, request, *arg, **kwargs):
		
		try:
			objeto = self.get_object()
			objeto.Status = False
			objeto.save()
			self.MensajeListAdd(mensaje_user = 'El Producto a sido eliminado exitosamente')
		except Exception as e:
			self.MensajeListAdd(mensaje_server  = str(e))
		return Response(self.salida(), status=200)
