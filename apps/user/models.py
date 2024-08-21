import uuid
from django.db import models
from apps.system.models import basemodel
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin



	

class UserManager(BaseUserManager):
	""" Modelo que hereda de la clase base que usa django para generar 
	los usuarios, de esta forma podemos personalizar los campos 
	necesarios para generar el usuario que creamos en la consola
	con el comando "python manage.py createsuperuser" """

	def _create_user(self, email, password, 
					is_staff, is_superuser, **extra_field):

		if not email:
			raise ValueError("El campo email es necesario")
		email = self.normalize_email(email)
		user = self.model(email=email, is_active=True, is_staff=is_staff,
							is_superuser=is_superuser, **extra_field)
		user.password=password
		user.Tipo="Admin"
		user.save(using = self._db)

		return user

	def create_user(self, email, password=None, **extra_field):
		return self._create_user(email, password, False, False,  **extra_field)

	def create_superuser(self, email, password, **extra_field):
		return self._create_user(email, password, True, True,  **extra_field)


class user(AbstractBaseUser, PermissionsMixin):

	""" Modelo usado para generar al usuario que se maneja en el contexto de la
	plataforma.
	Hereda propiedades de  AbstractBaseUser  y PermissionsMixin para que el modelo
	a pesar de ser personalizado pueda ser usado por django en sus subrutinas de 
	verificación y validación. """

	pk_publica = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	Creado = models.DateTimeField(auto_now_add=True)
	Modificado =models.DateTimeField(auto_now=True)
	username = models.CharField(max_length=15)
	email = models.EmailField(max_length=50, unique=True)
	is_staff = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)

	Status = models.BooleanField(default=True)
	Nombre_completo = models.CharField(max_length=60, default="")
	Nombres = models.CharField(max_length=50, default="")
	Apellidos = models.CharField(max_length=50, default="")
	Contacto = models.CharField(max_length=50, default="")
	Comentarios = models.CharField(max_length=200, default="")
	Tipos = (('Admin','Admin'), ('Coordinador','Coordinador'), ('Servicio','Servicio'), ('Almacen','Almacen'))
	Tipo = models.CharField(max_length=20, choices=Tipos, default='Coordinador')
	Codigo = models.CharField(max_length=60, blank=True, null=True)
   

	objects = UserManager() 

	USERNAME_FIELD = 'email'

	# REQUIRED_FIELDS = ['email']

	def get_short_name(self):
		return self.username

	
	def permisos():

		permisos = {
			'Admin' : ('get','post','update', 'delete', 'put'),
			'Coordinador' : ('get','post','update', 'delete', 'put'),
			'Servicio' : ('get','post','update', 'delete', 'put'),
		}
		return permisos

class Token(basemodel):


	token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	user = models.ForeignKey(user,
								related_name="Token", 
								null=True, 
								blank=True, 
								on_delete=models.CASCADE)
	def permisos():

		permisos = {
			'Admin' : ('get','post','update', 'delete'),
			'Coordinador' : ('get','post','update', 'delete'),
			'Servicio' : ('get','post','update', 'delete'),
		}

		return permisos
	

