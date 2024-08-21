from django.shortcuts import render

# Create your views here.
import re
import os
import jwt
import string
import secrets
from dateutil import tz
from django.db.models import Q
from django.db.models import F
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.contrib.auth import login as loginAut
from django.contrib.sessions.backends.db import SessionStore


import time
from datetime import datetime


from apps.system.models import login

from apps.system.utilis import get_public_key, get_private_key
from apps.system.ManageApi import ErrorManagerMixin
from apps.system.monitor import MonitorMixin
from django.core.paginator import Paginator
from .serializers import UsuarioSerializer, LoginSerializer
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from random import randint
from .models import user, Token

class LoginUserAPI(ErrorManagerMixin,CreateAPIView, APIView):
    
	serializer_class = LoginSerializer
	model = login
	def dispatch(self, request, *args, **kwargs):
		
		return super().dispatch(request, *args, **kwargs)
	def post(self, request, *arg, **kwargs):
		"""DDDDDDDDDDDD"""
		
		e = ''
	
		try:
			
			if  'email' not in request.data.keys():
				self.MensajeListAdd( mensaje_user = {'mensaje':'No estas enviando correctamente el email'}, 
								 status='error')
				return Response(self.salida(), status=500)

			if  'password' not in request.data.keys():
				self.MensajeListAdd( mensaje_user = {'mensaje':'No estas enviando correctamente el password'}, 
								 status='error')
				return Response(self.salida(), status=500)
		except Exception as e:
			self.MensajeListAdd( mensaje_user = {'mensaje':'No estas enviando correctamente el passsword y username'}, 
								 status='error')
			return Response(self.salida(), status=500)
		
		email =  request.data['email']
		password =  request.data['password']
		print(email, password)
		try:
			usermodel = user.objects.filter(Q(email=email)&Q(password=password))
			usuario = usermodel.first()
			if usermodel.count() == 0:
				self.MensajeListAdd(mensaje_user =  {'mensaje':'Usuario o contraseña invalida'}, status='warning')
				return Response(self.salida(), status=200)
			else:
				try:
					tokens = Token.objects.filter(user =  usuario, Status=True)
					for tok in tokens:
						tok.Status = False
						tok.save()

				except Exception as e:
				
					self.MensajeListAdd(mensaje_server  = str(e))
					return Response(self.salida(), status=500)

					
				token = Token(user = usuario)
				token.save()
				key = settings.SECRET_KEY_TOKEN
				encoded = jwt.encode({'token' : str(token.token), 'pk_publica': str(usuario.pk_publica)}, key, algorithm="HS256")
				
				jsonresp = {
					'token' : encoded
				}
				self.MensajeListAdd(mensaje_user = {'mensaje':'iniciando sesion'}, status='success')
				self.JsonAdd(json=jsonresp)
				
		
				return Response(self.salida(), status=200)
		except Exception as e:
			self.MensajeListAdd( mensaje_server = str(e))
			return Response(self.salida(), status=500)
			
		
	def __str__(self):
		return 'LoginUserAPI'

class LogoutUserApi(ErrorManagerMixin, APIView):
	

	def get(self, request, *arg, **kwargs):
		""" Obtiene los datos que corresponden al token """
		try:
				
			tokenJWTENCODE = request.headers.get('Authorization', '').replace('Bearer', '').strip()
			tokenJWTDECODE = jwt.decode(tokenJWTENCODE, settings.SECRET_KEY_TOKEN , algorithms="HS256")
			token = tokenJWTDECODE['token']
			utc = tz.tzutc()
			local = tz.tzlocal()
			token = Token.objects.get(token=token)
			
			fecha2 = datetime.now()

			ultima_peticion = str(token.Modificado)
			fecha1 = token.Modificado.replace(tzinfo=utc)
			fecha1 = fecha1.astimezone(local)

			diferencia = time.mktime(fecha2.timetuple()) - time.mktime(fecha1.timetuple()) 

			if diferencia > (60*60*6):

				self.MensajeListAdd( mensaje_user = 'Su sesion a expirado')
				token.Status = False
				token.save()
				
			else:
				token.Modificado = datetime.now()
				token.save()
				permisos = token.user.Tipo

				self.JsonAdd(json = {
					'ambito': permisos,
					'ultima_peticion':ultima_peticion,
					'Status': token.Status,
					'usuario': token.user.username,
					})
		except Exception as e:
			self.MensajeListAdd( mensaje_user = 'No autorizado',
				mensaje_server="No autorizado",
				status= 303)
			# print(request.session.keys())
			# print(self.salida())
			# return False
		return Response(self.salida(), status=200)
	def post(self, request, *arg, **kwargs):
		""" Cierra sesion del token que has pasado """
		# token = request.data['token']
		tokenJWTENCODE = request.headers.get('Authorization', '').replace('Bearer', '').strip()
		tokenJWTDECODE = jwt.decode(tokenJWTENCODE, settings.SECRET_KEY_TOKEN , algorithms="HS256")
		token = tokenJWTDECODE['token']

		try:
			token = Token.objects.get(token=token)
			token.Status = False
			token.save()
			self.MensajeListAdd(mensaje_user = 'Sesion finalizada')

		except Exception as e:
			self.MensajeListAdd( mensaje_server = str(e))
			return Response(self.salida(), status=404)
		
		return Response(self.salida(), status=200)
	



class AdminUserApi(MonitorMixin, CreateAPIView, ListAPIView, 
	RetrieveAPIView, UpdateAPIView, DestroyAPIView, APIView):
	serializer_class = UsuarioSerializer
	model= user
	def post(self, request, *arg, **kwargs):
		if 'email' not in request.data.keys():
			self.MensajeListAdd( mensaje_user = 'Ocurrio un error al procesar la solicitud', 
						mensaje_server='No estas enviando correctamente el email', status='error')
			return Response(self.salida(), status=200)

		if 'password' not in request.data.keys():
			self.MensajeListAdd( mensaje_user = 'Ocurrio un error al procesar la solicitud', 
						mensaje_server='No estas enviando correctamente el password', status='error')
			return Response(self.salida(), status=200)
		
		if 'username' not in request.data.keys():
			self.MensajeListAdd( mensaje_user = 'Ocurrio un error al procesar la solicitud', 
						mensaje_server='No estas enviando correctamente el username', status='error')
			return Response(self.salida(), status=200)
		# request.data['username'] =request.data['email']

		UsuarioSerializerresponse = UsuarioSerializer(data= request.data) 
		if UsuarioSerializerresponse.is_valid():
			# UsuarioSerializerresponse.instance.
			alphabet = string.ascii_letters + string.digits
			code = ''.join(secrets.choice(alphabet) for i in range(8))
			print(UsuarioSerializerresponse.validated_data)
			# UsuarioSerializerresponse.validated_data['password'] = make_password(UsuarioSerializerresponse.validated_data['password'])
			UsuarioSerializerresponse.validated_data['Codigo'] = code
			UsuarioSerializerresponse.validated_data['Nombre_completo'] = UsuarioSerializerresponse.validated_data['Nombres']+" "+ UsuarioSerializerresponse.validated_data['Apellidos']
			UsuarioSerializerresponse.save()
			print(os.environ.get("PRIVATE_BACK_URL"))
			with open(get_private_key(), "rb") as f:
				private_key = f.read()
			# with open("apps/system/public_back.pem", "rb") as f:
			# 	public_key = f.read()
			encoded = jwt.encode({"pas":UsuarioSerializerresponse.validated_data['password'] }, private_key, algorithm=settings.ALGORITM_ENCAP_BACK)

			
			# print(UsuarioSerializerresponse.instance.pk_publica)
			self.JsonAdd(json={
				"Nombres":UsuarioSerializerresponse.data['Nombres'],
				"Apellidos":UsuarioSerializerresponse.data['Apellidos'],
				"username":UsuarioSerializerresponse.data['username'],
				"Tipo":UsuarioSerializerresponse.data['Tipo'],
				"Contacto":UsuarioSerializerresponse.data['Contacto'],
			})
			self.MensajeListAdd( mensaje_user = {'mensaje':'Ahora puedes iniciar sesión'}, 
						mensaje_server=UsuarioSerializerresponse.errors, status='success')
			print()
			return Response(self.salida(), status=200)
		else:
			
			self.MensajeListAdd( mensaje_user = UsuarioSerializerresponse.errors, 
						mensaje_server=UsuarioSerializerresponse.errors, status='error')
			# self.JsonAdd(json=UsuarioSerializerresponse.errors)
			# print(UsuarioSerializerresponse.errors)
			return Response(self.salida(), status=200)
	
	def get(self, request, *arg, **kwargs):
		""" Enviar por get "pk" con la clave primaria del registro a buscar, el no enviar este valor implica la obtencion
		 de todos los registros del usuario en cuestion de ser asi enviar: \n
			count: numero de elmentos por pagina \n
		    page: numero de pagina \n
			usuario: codigo escaneado \n
			
			"""
		usuario = self.get_user()
	
		usuario_serh = request.GET.get('usuario')
		if usuario_serh != None:
			query =  self.model.objects.filter(Status=True, Nombre_completo__contains=usuario_serh)
			if query.count() == 0:
				self.MensajeListAdd(mensaje_user = 'El Usuario no existe',
						mensaje_server = 'El Usuario no existe o no pertenece al usuario relacionado con el token o el pk')			
				return Response(self.salida(), status=200)
			else:
				f = self.serializer_class(query, many=True)
				self.JsonAdd(json=f.data)			
				return Response(self.salida(), status=200)
		
		query =  self.model.objects.filter(Status=True)
		try:
			
			if self.pk_publica is None:
				if query is not None:
					total_count = query.count()
					if self.count and self.page:
					
						paginacion= Paginator(query,self.count)
						
						if len(paginacion.page(1)) == 0:
							pass
						else:
							query = paginacion.page(self.page)
					
					
					f = self.serializer_class(query, many=True)
					data = []
					for a in f.data:
						a['password'] = "**********************"
						data.append(a)
					
					self.JsonAdd(json={
						"total_count":total_count,
						"data":data
						})
				else:
					self.MensajeListAdd(mensaje_user = 'No hay registros')
				return Response(self.salida(), status=200)
			else:
				try:

					query =  self.model.objects.get(pk_publica=self.pk_publica, Status=True)
					f = self.serializer_class(query)
					self.JsonAdd(json=f.data)			
					return Response(self.salida(), status=200)
				except self.model.DoesNotExist:
					self.MensajeListAdd(mensaje_user = 'El Usuario no existe',
						mensaje_server = 'El Usuario no existe o es accesible al usuario relacionado con el token')			
					return Response(self.salida(), status=200)
				
		except Exception as e:
			self.MensajeListAdd(mensaje_server  = str(e))
			return Response(self.salida(), status=500)
	def delete(self, request, *arg, **kwargs):
		
		try:
			objeto = self.model.objects.get(pk_publica=self.pk_publica)
			objeto.Status = False
			objeto.save()
			self.MensajeListAdd(mensaje_user = 'El usuario a sido eliminado exitosamente')
		except Exception as e:
			self.MensajeListAdd(mensaje_server  = str(e))

		return Response(self.salida(), status=200)
	
	def update(self, request, *arg, **kwargs):
		try:
			if self.pk_publica is None:
				self.MensajeListAdd(mensaje_user='Ocurrieron errores al momento de guardar el Usuario',
				mensaje_server='No se a enviado correctamente la variable "pk" correspondiente al objeto a actualizar en la URL', status='error')
				return Response(self.salida(), status=303)
			else:
				try:
					usuario = self.get_user()
					print(usuario.Tipo)
					if usuario.Tipo != "Admin" and usuario.pk_publica!=self.pk_publica:
						self.MensajeListAdd( mensaje_user = 'No autorizado',
								mensaje_server="No autorizado",
								status= 303)
						return Response(self.salida(), status=303)
					else:
						objeto = self.model.objects.get(pk_publica=self.pk_publica,
						Status=True )
				except self.model.DoesNotExist:
					self.MensajeListAdd(mensaje_user = 'Ocurrieron uno o mas errores a actualizar el Usuario',
						mensaje_server = 'El objeto no existe o no pertenece al usuario al que esta relacionado al token')
					return Response(self.salida(), status=404)
				
				usuarioserializer = self.serializer_class( objeto, data= request.data, partial=True)
				if usuarioserializer.is_valid():
					usuarioserializer.save()
					self.MensajeListAdd(mensaje_user='Producto guardado con exito', status='success')
					self.JsonAdd(json = usuarioserializer.data )
					return Response( self.salida(), status=200)
				else:
					self.JsonAdd(json = usuarioserializer.errors )
					self.MensajeListAdd(mensaje_user='Ocurrieron errores al momento de guardar el Usuario',
						mensaje_server=usuarioserializer.errors, status='error')

					return Response(self.salida(), status=200)
		except Exception as e:
			self.MensajeListAdd(mensaje_server  = str(e))
			return Response(self.salida(), status=500)


