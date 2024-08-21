from django.db import models
from apps.system.models import basemodel
from apps.user.models import user
from apps.producto.models import Producto


class retiro(basemodel):

    retira = models.ForeignKey(user,
		related_name="quienretiro", 
		 
		on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto,
		related_name="retiroproducto", 
		null=False, 
		blank=False, 
		on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=0)


class deposito(basemodel):
    deposita = models.ForeignKey(user,
		related_name="quiendeposita", 
		null=False, 
		blank=False, 
		on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto,
		related_name="depoproducto", 
		null=False, 
		blank=False, 
		on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=0)
