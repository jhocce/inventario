from django.urls import path
from .views import  AdminUserApi, LogoutUserApi, LoginUserAPI



urlpatterns = [
	path('', AdminUserApi.as_view(), name="AdminUserApi"),
	path('login/', LoginUserAPI.as_view(), name="login"),
    path('logout/', LogoutUserApi.as_view(), name="logout"),	
]