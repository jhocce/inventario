from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi



schema_view = get_schema_view(
   openapi.Info(
      title="Base API",
      default_version='v1',
      description="Tprueba",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="jhocce3022@hotmail.com"),
      license=openapi.License(name="null"),
   ),
   public=True,
   # permission_classes=[permissions.AllowAny],
)


#  http://128.199.8.62/.well-known/pki-validation/12E7C08C8BF0A711D7564903863CD2E2.txt
urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('user/', include(('apps.user.urls', 'user'), namespace="user")),
    path('producto/', include(('apps.producto.urls', 'producto'), namespace="producto")),
    path('almacen/', include(('apps.almacen.urls', 'almacen'), namespace="almacen")),
    
    path('api-auth/', include('rest_framework.urls'))
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
