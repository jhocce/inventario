from django.shortcuts import render
import qrcode
import json
import string
import secrets
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

from .serializers import retiroSerializer, depositoSerializer
from .models import retiro, deposito
from apps.user.models import user
from apps.producto.models import Producto

class retiroAPI(MonitorMixin,CreateAPIView, ListAPIView, 
	 APIView):
	
	serializer_class = retiroSerializer
	model = retiro

	def post(self, request, *arg, **kwargs):
		
		try:
			serviciosSerializer = self.serializer_class(data= request.data)
			if serviciosSerializer.is_valid():
				
				try:
					us = user.objects.get(pk_publica=request.data['retira']['pk_publica'])
				except user.DoesNotExist:
					self.MensajeListAdd(mensaje_user='Usuario no encontrado', status='error')
					return Response( self.salida(), status=200)
				serviciosSerializer.validated_data['retira'] = us
				cantidad = serviciosSerializer.validated_data['cantidad']
				pk_prd = request.data['producto']['pk_publica']

				try:
					l = Producto.objects.get(pk_publica=pk_prd)
					if l.Cantidad< cantidad:
						self.MensajeListAdd(mensaje_user='No hay suficiente cantidad en deposito', status='error')
						return Response( self.salida(), status=200)
					else:
						l.Cantidad = l.Cantidad - cantidad
						l.save()
						serviciosSerializer.validated_data['producto']=l
				except Exception as e:
					self.MensajeListAdd(mensaje_user='Producto no existe', status='error')
					return Response( self.salida(), status=200)
				serviciosSerializer.save()
				self.MensajeListAdd(mensaje_user='Retiro Guardado Exitosamente', status='success')
	
				data = dict(serviciosSerializer.data)
				self.JsonAdd(json = data )
				return Response( self.salida(), status=200)

			else:
				self.JsonAdd(json = serviciosSerializer.errors )
				self.MensajeListAdd(mensaje_user='Ocurrieron errores al momento de guardar el retiro',
					mensaje_server=serviciosSerializer.errors, status='error')
				return Response(self.salida(), status=200)

		except Exception as e:
			
			self.MensajeListAdd(mensaje_user='Ocurrieron errores al momento de guardar el retiro', mensaje_server  = str(e))
			return Response(self.salida(), status=500)
		
	def get(self, request, *arg, **kwargs):
		""" Enviar por get "pk" con la clave primaria del registro a buscar, el no enviar este valor implica la obtencion
		 de todos los registros del usuario en cuestion de ser asi enviar: \n
			count: numero de elmentos por pagina \n
			page: numero de pagina \n
			
			"""
		try:

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
					f = self.serializer_class(query, many=True)
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
				query =  self.model.objects.get(Status=True, pk_publica=self.pk_publica)
				
				if query is None:
					self.MensajeListAdd(mensaje_user = 'El retiro no existe',
						mensaje_server = 'El retiro no existe o no pertenece al usuario relacionado con el token o el pk')			
					return Response(self.salida(), status=200)
				else:
					f = self.serializer_class(query)
					self.JsonAdd(json=f.data)			
					return Response(self.salida(), status=200)

		except Exception as e:
			self.MensajeListAdd(mensaje_server  = str(e))
			return Response(self.salida(), status=500)

class depositoAPI(MonitorMixin,CreateAPIView, ListAPIView, 
	 APIView):
	
	serializer_class = depositoSerializer
	model = deposito
	
	def post(self, request, *arg, **kwargs):
		
		try:
			serviciosSerializer = self.serializer_class(data= request.data)
			if serviciosSerializer.is_valid():
				
				try:
					us = user.objects.get(pk_publica=request.data['deposita']['pk_publica'])
				except user.DoesNotExist:
					self.MensajeListAdd(mensaje_user='Usuario no encontrado', status='error')
					return Response( self.salida(), status=200)
				serviciosSerializer.validated_data['deposita'] = us
				cantidad = serviciosSerializer.validated_data['cantidad']
				pk_prd = request.data['producto']['pk_publica']

				try:
					l = Producto.objects.get(pk_publica=pk_prd)
					
					l.Cantidad = l.Cantidad + cantidad
					l.save()
					serviciosSerializer.validated_data['producto']=l
				except Exception as e:
					self.MensajeListAdd(mensaje_user='Producto no existe', status='error')
					return Response( self.salida(), status=200)
				serviciosSerializer.save()
				self.MensajeListAdd(mensaje_user='deposito Guardado Exitosamente', status='success')
	
				data = dict(serviciosSerializer.data)
				self.JsonAdd(json = data )
				return Response( self.salida(), status=200)

			else:
				self.JsonAdd(json = serviciosSerializer.errors )
				self.MensajeListAdd(mensaje_user='Ocurrieron errores al momento de guardar el deposito',
					mensaje_server=serviciosSerializer.errors, status='error')
				return Response(self.salida(), status=200)

		except Exception as e:
			
			self.MensajeListAdd(mensaje_user='Ocurrieron errores al momento de guardar el deposito', mensaje_server  = str(e))
			return Response(self.salida(), status=500)
		
	def get(self, request, *arg, **kwargs):
		""" Enviar por get "pk" con la clave primaria del registro a buscar, el no enviar este valor implica la obtencion
		 de todos los registros del usuario en cuestion de ser asi enviar: \n
			count: numero de elmentos por pagina \n
			page: numero de pagina \n
			
			"""
		try:

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
					f = self.serializer_class(query, many=True)
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
				query =  self.model.objects.get(Status=True, pk_publica=self.pk_publica)
				
				if query is None:
					self.MensajeListAdd(mensaje_user = 'El deposito no existe',
						mensaje_server = 'El deposito no existe o no pertenece al usuario relacionado con el token o el pk')			
					return Response(self.salida(), status=200)
				else:
					f = self.serializer_class(query)
					self.JsonAdd(json=f.data)			
					return Response(self.salida(), status=200)

		except Exception as e:
			self.MensajeListAdd(mensaje_server  = str(e))
			return Response(self.salida(), status=500)

