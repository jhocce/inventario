from django.urls import path
from .views import  ProductoAPI



urlpatterns = [
	path('', ProductoAPI.as_view(), name="ProductoAPI"),
]