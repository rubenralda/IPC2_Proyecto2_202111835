from django.urls import path
from . import views

urlpatterns = [
    path('cargar/',views.cargar, name='configuracion'),
    path('consultaDatos/',views.consultar_datos, name='consulta'),
    path('factura/',views.factura, name='factura'),
    path('crearEmpresa/',views.crear_empresa, name='crearEmpresa'),
] 