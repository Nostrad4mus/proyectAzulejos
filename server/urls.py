"""
URL configuration for server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from client import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.see_home),
    path('azulejos-figurativos', views.see_explaining),
    path('catalogo', views.see_catalogo),
    path('catalogo/<str:tipo>', views.see_azulejo),
    path('rutas', views.see_rutas),
    path('librery', views.see_librery),
    path('about', views.see_about),
    path('guia-infantil', views.see_child_zone),
    path('actividad/patrones', views.see_child_patrones),
    path('actividad/cuentos', views.see_child_historias),
    path('actividad/cuentos/<slug:slug>', views.see_cuento),
    path('actividad/taller', views.see_talleres),
    path('actividad/taller/<slug:slug>', views.see_taller),
    path('actividad/tesoro', views.see_treasure_search),
    path('actividad/tesoro/get_random_tile/', views.get_random_tile),
    path('actividad/rompecabezas', views.see_rompecabezas),
    path('rompecabezas/get_random_tile/', views.get_random_tile, name='get_random_tile'),
    path('actividad/descargables', views.see_child_librery),
    path('info-padres/', views.see_child_faders),
    path('contacto/', views.see_contacto),
]
