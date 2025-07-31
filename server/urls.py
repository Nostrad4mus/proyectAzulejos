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
    
    
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # URLs para Azulejos
    path('admin-dashboard/azulejos/', views.admin_azulejos, name='admin_azulejos'),
    path('admin-dashboard/azulejos/crear/', views.crear_azulejo, name='crear_azulejo'),
    path('admin-dashboard/azulejos/<int:pk>/editar/', views.editar_azulejo, name='editar_azulejo'),
    path('admin-dashboard/azulejos/<int:pk>/eliminar/', views.eliminar_azulejo, name='eliminar_azulejo'),
    path('admin-dashboard/azulejos/eliminar-multiples/', views.eliminar_azulejos_multiples, name='eliminar_azulejos_multiples'),
    
    # URLs para Recursos
    path('admin-dashboard/recursos/', views.admin_recursos, name='admin_recursos'),
    path('admin-dashboard/recursos/crear/', views.crear_recurso, name='crear_recurso'),
    path('admin-dashboard/recursos/<int:pk>/editar/', views.editar_recurso, name='editar_recurso'),
    path('admin-dashboard/recursos/<int:pk>/eliminar/', views.eliminar_recurso, name='eliminar_recurso'),
    path('admin-dashboard/recursos/eliminar-multiples/', views.eliminar_recursos_multiples, name='eliminar_recursos_multiples'),

    # Miembros del Equipo
    path('admin-dashboard/miembros/', views.admin_miembros, name='admin_miembros'),
    path('admin-dashboard/miembros/crear/', views.crear_miembro, name='crear_miembro'),
    path('admin-dashboard/miembros/<int:pk>/editar/', views.editar_miembro, name='editar_miembro'),
    path('admin-dashboard/miembros/<int:pk>/eliminar/', views.eliminar_miembro, name='eliminar_miembro'),
    
    # Cuentos Animados
    path('admin-dashboard/cuentos/', views.admin_cuentos, name='admin_cuentos'),
    path('admin-dashboard/cuentos/crear/', views.crear_cuento, name='crear_cuento'),
    path('admin-dashboard/cuentos/<int:pk>/editar/', views.editar_cuento, name='editar_cuento'),
    path('admin-dashboard/cuentos/<int:pk>/eliminar/', views.eliminar_cuento, name='eliminar_cuento'),
    
    # Talleres Creativos
    path('admin-dashboard/talleres/', views.admin_talleres, name='admin_talleres'),
    path('admin-dashboard/talleres/crear/', views.crear_taller, name='crear_taller'),
    path('admin-dashboard/talleres/<int:pk>/editar/', views.editar_taller, name='editar_taller'),
    path('admin-dashboard/talleres/<int:pk>/eliminar/', views.eliminar_taller, name='eliminar_taller'),
    
    
    # Perfil y Configuración
    path('admin-dashboard/perfil/', views.perfil_usuario, name='perfil_usuario'),
    path('admin-dashboard/configuracion/', views.configuracion_usuario, name='configuracion_usuario'),
    
    
    # Login
    path('admin-dashboard/login/', views.CustomLoginView.as_view(), name='login'),
    
    # Logout
    path('admin-dashboard/logout/', views.CustomLogoutView.as_view(), name='logout'),

    
    path('admin-dashboard/gestion-usuarios/', views.gestion_usuarios, name='gestion_usuarios'),
    path('admin-dashboard/gestion-usuarios/crear/', views.crear_usuario, name='crear_usuario'),
    path('admin-dashboard/gestion-usuarios/<int:pk>/editar/', views.editar_usuario, name='editar_usuario'),
    path('admin-dashboard/gestion-usuarios/<int:pk>/eliminar/', views.eliminar_usuario, name='eliminar_usuario'),
    
    
    # path('admin/', admin.site.urls),
]
