from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Azulejo(models.Model):
    
    ESTILOS = [
    ('COL', _('Colonial')),
    ('BAR', _('Barroco')),
    ('NEO', _('Neoclásico')),
    ('ART', _('Art Nouveau')),
    ('DEC', _('Art Déco')),
    ('MOD', _('Moderno')),
    ('CON', _('Contemporáneo')),
    ]

    
    titulo = models.CharField(max_length=100, blank=True, default="")
    descripcion = models.TextField(default="")
    imagen = models.ImageField(upload_to='client/static/img/azulejos', blank=True, null=True)
    latitud = models.DecimalField(
        max_digits=9, 
        decimal_places=6,
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
        default=0
    )
    longitud = models.DecimalField(
        max_digits=9, 
        decimal_places=6,
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
        default=0
    )
    
    nombre = models.CharField(_('Nombre'), max_length=100, blank=True, default="")
    descripcion = models.TextField(_('Descripción'), blank=True, default="")
    estilo = models.CharField(_('Estilo'), max_length=3, choices=ESTILOS, blank=True, default="")
    epoca = models.CharField(_('Época'), max_length=50, blank=True, default="")
    ubicacion = models.CharField(_('Ubicación'), max_length=200, blank=True, default="")
    imagen_principal = models.ImageField(_('Imagen principal'), upload_to='client/static/img/catalogo', blank=True, default="")
    imagen_detalle = models.ImageField(_('Imagen detalle'), upload_to='client/static/img/catalogo', blank=True, null=True)
    # fecha_documentacion = models.DateField(_('Fecha de documentación'), blank=True, auto_now=True)
    coleccion = models.CharField(_('Colección'), max_length=100, blank=True)
    
    
    def __str__(self):
        return self.titulo
    
    class Meta:
        verbose_name = "Ubicación de Azulejo"
        verbose_name_plural = "Ubicaciones de Azulejos"

import os
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator
from django.utils.text import slugify
from django.dispatch import receiver
from django.db.models.signals import pre_save

class RecursoBibliografico(models.Model):
    TIPO_CHOICES = [
        ('LIB', _('Libro')),
        ('ART', _('Artículo')),
        ('TES', _('Tesis')),
        ('DOC', _('Documento')),
        ('VID', _('Video')),
        ('IMG', _('Imagen')),
        ('AUD', _('Audio')),
        ('OTR', _('Otro')),
    ]

    AREA_CHOICES = [
        ('HIS', _('Historia')),
        ('TEC', _('Técnica')),
        ('RES', _('Restauración')),
        ('ART', _('Artístico')),
        ('ARQ', _('Arquitectónico')),
        ('SOC', _('Social')),
        ('CUL', _('Cultural')),
    ]

    titulo = models.CharField(_('Título'), max_length=200)
    autor = models.CharField(_('Autor(es)'), max_length=200)
    descripcion = models.TextField(_('Descripción'))
    archivo = models.FileField(
        _('Archivo'), 
        upload_to='client/static/documents/',
        validators=[FileExtensionValidator(
            allowed_extensions=['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png', 'mp4', 'avi', 'mov', 'mp3']
        )]
    )
    tipo = models.CharField(_('Tipo'), max_length=3, choices=TIPO_CHOICES, blank=True)
    area = models.CharField(_('Área temática'), max_length=3, choices=AREA_CHOICES, blank=True)
    fecha_publicacion = models.DateField(_('Fecha de publicación'), blank=True, null=True)
    fecha_subida = models.DateTimeField(_('Fecha de subida'), auto_now_add=True)
    isbn = models.CharField(_('ISBN'), max_length=20, blank=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    vista_previa = models.ImageField(_('Vista previa'), upload_to='client/static/documents/previews/', blank=True, null=True)

    class Meta:
        verbose_name = _('Recurso bibliográfico')
        verbose_name_plural = _('Recursos bibliográficos')
        ordering = ['-fecha_subida']

    def __str__(self):
        return self.titulo

    def get_extension(self):
        name, extension = os.path.splitext(self.archivo.name)
        return extension[1:].upper()  # Quita el punto y convierte a mayúsculas

    def get_icon_class(self):
        extension = self.get_extension().lower()
        if extension in ['pdf']:
            return 'bi bi-file-earmark-pdf'
        elif extension in ['doc', 'docx']:
            return 'bi bi-file-earmark-word'
        elif extension in ['jpg', 'jpeg', 'png']:
            return 'bi bi-file-image'
        elif extension in ['mp4', 'avi', 'mov']:
            return 'bi bi-file-play'
        elif extension in ['mp3']:
            return 'bi bi-file-music'
        else:
            return 'bi bi-file-earmark'

    def get_file_size(self):
        try:
            size_bytes = self.archivo.size
            # Convertir a MB
            size_mb = size_bytes / (1024 * 1024)
            return f"{size_mb:.2f} MB"
        except:
            return "N/A"

@receiver(pre_save, sender=RecursoBibliografico)
def set_slug_and_type(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.titulo)
    
    # Detectar tipo automáticamente por extensión si no está definido
    if not instance.tipo:
        extension = instance.get_extension().lower()
        if extension in ['pdf', 'doc', 'docx']:
            instance.tipo = 'DOC' if extension != 'pdf' else 'LIB'
        elif extension in ['jpg', 'jpeg', 'png']:
            instance.tipo = 'IMG'
        elif extension in ['mp4', 'avi', 'mov']:
            instance.tipo = 'VID'
        elif extension in ['mp3']:
            instance.tipo = 'AUD'
        else:
            instance.tipo = 'OTR'

class MiembroEquipo(models.Model):
    ROL_CHOICES = [
        ('INV', _('Investigador')),
        ('ARQ', _('Arquitecto')),
        ('HIS', _('Historiador')),
        ('DES', _('Diseñador')),
        ('DEV', _('Desarrollador')),
        ('FOT', _('Fotógrafo')),
        ('ADM', _('Administrador')),
        ('COL', _('Colaborador')),
    ]
    
    nombre = models.CharField(_('Nombre completo'), max_length=100)
    rol = models.CharField(_('Rol principal'), max_length=3, choices=ROL_CHOICES)
    rol_secundario = models.CharField(_('Rol secundario'), max_length=3, choices=ROL_CHOICES, blank=True, null=True)
    biografia = models.TextField(_('Biografía profesional'))
    imagen = models.ImageField(_('Foto de perfil'), upload_to='client/static/img/equipo/')
    email = models.EmailField(_('Correo electrónico'))
    telefono = models.CharField(_('Teléfono'), max_length=20, blank=True)
    orden = models.PositiveIntegerField(_('Orden de aparición'), default=0)
    
    # Redes sociales
    facebook = models.URLField(_('Facebook'), blank=True)
    instagram = models.URLField(_('Instagram'), blank=True)
    twitter = models.URLField(_('Twitter (X)'), blank=True)
    linkedin = models.URLField(_('LinkedIn'), blank=True)
    github = models.URLField(_('GitHub'), blank=True)
    telegram = models.URLField(_('Telegram'), blank=True)
    whatsapp = models.CharField(_('WhatsApp (número)'), max_length=20, blank=True)
    discord = models.CharField(_('Discord (usuario)'), max_length=50, blank=True)
    
    # Áreas de especialización
    especializacion = models.CharField(_('Especialización'), max_length=100)
    citacion_favorita = models.TextField(_('Citación favorita'), blank=True)
    proyectos_destacados = models.TextField(_('Proyectos destacados'), blank=True)
    
    class Meta:
        verbose_name = _('Miembro del equipo')
        verbose_name_plural = _('Miembros del equipo')
        ordering = ['orden', 'nombre']
    
    def __str__(self):
        return self.nombre
    
    def redes_sociales(self):
        redes = []
        if self.facebook: redes.append(('facebook', self.facebook, 'bi bi-facebook'))
        if self.instagram: redes.append(('instagram', self.instagram, 'bi bi-instagram'))
        if self.twitter: redes.append(('twitter', self.twitter, 'bi bi-twitter-x'))
        if self.linkedin: redes.append(('linkedin', self.linkedin, 'bi bi-linkedin'))
        if self.github: redes.append(('github', self.github, 'bi bi-github'))
        if self.telegram: redes.append(('telegram', self.telegram, 'bi bi-telegram'))
        if self.whatsapp: redes.append(('whatsapp', f'https://wa.me/{self.whatsapp}', 'bi bi-whatsapp'))
        if self.discord: redes.append(('discord', f'https://discord.com/users/{self.discord}', 'bi bi-discord'))
        return redes


class CuentoAnimado(models.Model):
    NIVEL_CHOICES = [
        ('P', _('Principiante')),
        ('I', _('Intermedio')),
        ('A', _('Avanzado')),
    ]
    
    titulo = models.CharField(_('Título'), max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    descripcion = models.TextField(_('Descripción'))
    contenido = models.TextField(_('Contenido del cuento (HTML)'))
    portada = models.ImageField(_('Portada'), upload_to='client/static/cuentos/portadas/')
    archivo_animado = models.FileField(
        _('Archivo animado'),
        upload_to='client/static/cuentos/animaciones/',
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'webm', 'gif'])]
    )
    duracion = models.PositiveIntegerField(_('Duración (segundos)'))
    nivel = models.CharField(_('Nivel'), max_length=1, choices=NIVEL_CHOICES)
    fecha_publicacion = models.DateTimeField(_('Fecha de publicación'), auto_now_add=True)
    autor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    personaje_principal = models.CharField(
        _('Personaje principal'),
        max_length=20,
        choices=[('AZU', 'Azulejín'), ('AZA', 'Azulejina')],
        default='AZU'
    )
    likes = models.ManyToManyField(User, related_name='cuentos_like', blank=True)
    visitas = models.PositiveIntegerField(_('Visitas'), default=0)
    activo = models.BooleanField(_('Activo'), default=True)

    class Meta:
        verbose_name = _('Cuento animado')
        verbose_name_plural = _('Cuentos animados')
        ordering = ['-fecha_publicacion']

    def __str__(self):
        return self.titulo

    def total_likes(self):
        return self.likes.count()

    def incrementar_visitas(self):
        self.visitas += 1
        self.save()


class TallerCreativo(models.Model):
    NIVEL_DIFICULTAD = [
        ('F', _('Fácil')),
        ('M', _('Medio')),
        ('D', _('Difícil')),
    ]
    
    TIPO_TALLER = [
        ('VIR', _('Virtual')),
        ('PRE', _('Presencial')),
        ('HIB', _('Híbrido')),
    ]
    
    titulo = models.CharField(_('Título'), max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    descripcion = models.TextField(_('Descripción'))
    imagen_portada = models.ImageField(_('Imagen de portada'), upload_to='client/static/talleres/portadas/')
    video_tutorial = models.FileField(
        _('Video tutorial'),
        upload_to='client/static/talleres/videos/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'webm'])]
    )
    duracion_estimada = models.PositiveIntegerField(_('Duración estimada (min)'))
    nivel_dificultad = models.CharField(_('Nivel de dificultad'), max_length=1, choices=NIVEL_DIFICULTAD)
    tipo_taller = models.CharField(_('Tipo de taller'), max_length=3, choices=TIPO_TALLER)
    materiales_necesarios = models.TextField(_('Materiales necesarios'))
    fecha_publicacion = models.DateTimeField(_('Fecha de publicación'), auto_now_add=True)
    edad_recomendada_min = models.PositiveIntegerField(_('Edad mínima recomendada'), default=6)
    edad_recomendada_max = models.PositiveIntegerField(_('Edad máxima recomendada'), default=12)
    activo = models.BooleanField(_('Activo'), default=True)
    personaje_principal = models.CharField(
        _('Personaje principal'),
        max_length=3,
        choices=[('AZU', 'Azulejín'), ('AZA', 'Azulejina')],
        default='AZU'
    )
    
    class Meta:
        verbose_name = _('Taller creativo')
        verbose_name_plural = _('Talleres creativos')
        ordering = ['-fecha_publicacion']
    
    def __str__(self):
        return self.titulo
    
    def get_nivel_color(self):
        return {
            'F': '#4ECDC4',  # Verde agua
            'M': '#FFD166',  # Amarillo
            'D': '#FF6B6B'   # Rojo
        }.get(self.nivel_dificultad, '#26547C')  # Azul por defecto