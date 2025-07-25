from django.contrib import admin
from django.utils.html import format_html
from .models import Azulejo, RecursoBibliografico, MiembroEquipo, CuentoAnimado, TallerCreativo
# Register your models here.

admin.site.register(Azulejo)
# admin.site.register(CatalogoAzulejo)
# admin.site.register(Noticia)
admin.site.register(RecursoBibliografico)
admin.site.register(MiembroEquipo)



# class CuentoAnimadoAdmin(admin.ModelAdmin):
#     list_display = ('titulo', 'nivel', 'personaje_principal', 'fecha_publicacion', 'activo', 'portada_preview', 'total_likes')
#     list_filter = ('nivel', 'personaje_principal', 'activo')
#     search_fields = ('titulo', 'descripcion')
#     prepopulated_fields = {'slug': ('titulo',)}
#     readonly_fields = ('total_likes', 'visitas')
#     fieldsets = (
#         ('Información Básica', {
#             'fields': ('titulo', 'slug', 'descripcion', 'nivel', 'personaje_principal')
#         }),
#         ('Contenido', {
#             'fields': ('contenido', 'portada', 'portada_preview', 'archivo_animado', 'duracion')
#         }),
#         ('Estadísticas', {
#             'fields': ('total_likes', 'visitas')
#         }),
#         ('Publicación', {
#             'fields': ('activo', 'autor')
#         }),
#     )
    
#     def portada_preview(self, obj):
#         return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />'.format(obj.portada.url))
#     portada_preview.short_description = 'Vista previa'
    
#     def save_model(self, request, obj, form, change):
#         if not obj.autor:
#             obj.autor = request.user
#         super().save_model(request, obj, form, change)

admin.site.register(CuentoAnimado)
admin.site.register(TallerCreativo)