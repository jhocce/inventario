from django.urls import path
from .views import  retiroAPI, depositoAPI



urlpatterns = [
	path('retiro', retiroAPI.as_view(), name="retiroAPI"),
	path('depositar', depositoAPI.as_view(), name="depositoAPI"),
]