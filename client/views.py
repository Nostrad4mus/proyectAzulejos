from .models import Azulejo, RecursoBibliografico, MiembroEquipo, CuentoAnimado, TallerCreativo
from django.core.mail import send_mail, mail_admins, EmailMessage
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.utils.html import strip_tags
from django.http import JsonResponse
from django.contrib import messages
from django.conf import settings
from django.db.models import Q




import random

def clear_dir(recurso):
    recurso = str(recurso).replace('client/static/', '')
    return recurso

# Create your views here.
def see_home(req):
    azulejos = Azulejo.objects.all()
    return render(req, 'index.html', {
        "azulejos": azulejos
    })

def see_catalogo(req):
    
    # # Filtros
    estilo = req.GET.get('estilo')
    epoca = req.GET.get('epoca')
    color = req.GET.get('color')
    
    azulejos = Azulejo.objects.all()
    
    if estilo:
        azulejos = azulejos.filter(estilo=estilo)
    if epoca:
        azulejos = azulejos.filter(epoca__icontains=epoca)
    if color:
        azulejos = azulejos.filter(color_principal__icontains=color)
        
    for i in range(len(azulejos)):
        azulejos[i].imagen_detalle = str(azulejos[i].imagen_detalle).replace("client/static/", "")
        azulejos[i].imagen = str(azulejos[i].imagen).replace("client/static/", "")
    
    # Paginación
    paginator = Paginator(azulejos, 6)
    page_number = req.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    
    context = {
        'page_obj': page_obj,
        'estilos': Azulejo.ESTILOS,
        # 'colores': Azulejo.objects.values_list('color_principal', flat=True).distinct(),
        'epocas': Azulejo.objects.values_list('epoca', flat=True).distinct(),
    }
    
    
    
    return render(req, 'catalogo.html', context)

# def see_test(req):
#     # Obtener las 3 noticias más recientes
#     noticias = Noticia.objects.filter(destacada=True).order_by('-fecha_publicacion')[:3]
    
#     # Resto de tu lógica para otros contenidos
#     context = {
#         'noticias': noticias,
#         # ... otros contextos
#     }
#     return render(req, 'test.html', context)

# def todas_noticias(req):
#     noticias = Noticia.objects.all().order_by('-fecha_publicacion')
#     return render(req, 'noticias/todas.html', {'noticias': noticias})

# def detalle_noticia(req, id):
#     noticia = get_object_or_404(Noticia, id=id)
#     return render(req, 'noticias/detalle.html', {'noticia': noticia})


def see_rutas(req):
    azulejos = Azulejo.objects.all()
    
    for azulejo in azulejos:
        azulejo.imagen = str(azulejo.imagen).replace("client/static/", "")
        azulejo.longitud, azulejo.latitud = str(azulejo.longitud), str(azulejo.latitud)
    return render(req, 'mapa.html', {
        "azulejos": azulejos
    })


def see_azulejo(req, tipo):
    
    azulejo = get_object_or_404(Azulejo,id=tipo)
    azulejo.imagen = str(azulejo.imagen).replace("client/static/", "")
    azulejo.imagen_principal = str(azulejo.imagen_principal).replace("client/static/", "")
    azulejo.imagen_detalle = str(azulejo.imagen_detalle).replace("client/static/", "")

    return render(req, 'azulejo.html',{
        "azulejo":azulejo
    })

def see_explaining(req):
    
    
    return render(req, "explaining.html")

def see_librery(req):
    # Filtros
    tipo = req.GET.get('tipo')
    area = req.GET.get('area')
    busqueda = req.GET.get('q')
    
    recursos = RecursoBibliografico.objects.all()
    
    if tipo:
        recursos = recursos.filter(tipo=tipo)
    if area:
        recursos = recursos.filter(area=area)
    if busqueda:
        recursos = recursos.filter(
            models.Q(titulo__icontains=busqueda) |
            models.Q(autor__icontains=busqueda) |
            models.Q(descripcion__icontains=busqueda)
        )
    
    for recurso in recursos:
        recurso.archivo = str(recurso.archivo).replace('client/static/', '')
        recurso.vista_previa = str(recurso.vista_previa).replace('client/static/', '')
    
    # Paginación
    paginator = Paginator(recursos, 6)
    page_number = req.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    
    context = {
        'page_obj': page_obj,
        'tipos': RecursoBibliografico.TIPO_CHOICES,
        'areas': RecursoBibliografico.AREA_CHOICES,
        'filtro_tipo': tipo,
        'filtro_area': area,
        'busqueda': busqueda or '',
    }
    return render(req, 'bibliografia.html', context)

def see_about(req):
    miembros = MiembroEquipo.objects.all()
    
    for miembro in miembros:
        miembro.imagen = str(miembro.imagen).replace("client/static/", "")
    
    return render(req, 'about.html', {'miembros': miembros})


def see_child_zone(req):
    
    
    return render(req, 'child-zone.html')

def see_child_patrones(req):
    
    return render(req, 'child-patrones.html')
    

def see_child_historias(req):
    query = req.GET.get('q')
    nivel = req.GET.get('nivel')
    personaje = req.GET.get('personaje')
    
    cuentos = CuentoAnimado.objects.filter(activo=True)
    
    
    if query:
        cuentos = cuentos.filter(
            Q(titulo__icontains=query) |
            Q(descripcion__icontains=query)
        )
    
    if nivel:
        cuentos = cuentos.filter(nivel=nivel)
    
    if personaje:
        cuentos = cuentos.filter(personaje_principal=personaje)
    
    # Ordenar por más populares
    cuentos = cuentos.order_by('-visitas', '-fecha_publicacion')
    
    paginator = Paginator(cuentos, 9)
    page_number = req.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    for cuento in page_obj.object_list:
        cuento.portada = str(cuento.portada).replace("client/static/","")
        cuento.archivo_animado = str(cuento.archivo_animado).replace("client/static/","")
    
    
    context = {
        'page_obj': page_obj,
        'niveles': CuentoAnimado.NIVEL_CHOICES,
        'personajes': [('AZU', 'Azulejín'), ('AZA', 'Azulejina')],
        'filtro_nivel': nivel,
        'filtro_personaje': personaje,
        'busqueda': query or ''
    }
    return render(req, 'child-historias.html', context)

def see_cuento(req, slug):
    cuento = get_object_or_404(CuentoAnimado, slug=slug, activo=True)
    cuento.incrementar_visitas()
    
    cuento.portada = str(cuento.portada).replace("client/static/","")
    cuento.archivo_animado = str(cuento.archivo_animado).replace("client/static/","")
    
    context = {
        'cuento': cuento,
        'personaje_principal': 'Azulejín' if cuento.personaje_principal == 'AZU' else 'Azulejina'
    }
    return render(req, 'child-cuento.html', context)


def see_talleres(req):
    talleres = TallerCreativo.objects.filter(activo=True).order_by('-fecha_publicacion')
    
    for taller in talleres:
        taller.imagen_portada = str(taller.imagen_portada).replace("client/static/","")
        taller.video_tutorial = str(taller.video_tutorial).replace("client/static/", "")

    
    # Filtros
    nivel = req.GET.get('nivel')
    if nivel in ['F', 'M', 'D']:
        talleres = talleres.filter(nivel_dificultad=nivel)
    
    tipo = req.GET.get('tipo')
    if tipo in ['VIR', 'PRE', 'HIB']:
        talleres = talleres.filter(tipo_taller=tipo)
    
    personaje = req.GET.get('personaje')
    if personaje in ['AZU', 'AZA']:
        talleres = talleres.filter(personaje_principal=personaje)
    
    
    
    
    context = {
        'talleres': talleres,
        'filtro_nivel': nivel,
        'filtro_tipo': tipo,
        'filtro_personaje': personaje,
    }
    return render(req, 'child-talleres.html', context)

def see_taller(req, slug):
    
    taller = get_object_or_404(TallerCreativo, slug=slug, activo=True)
    
    # Materiales como lista
    materiales = [m.strip() for m in taller.materiales_necesarios.split('\n') if m.strip()]
    
    taller.video_tutorial = str(taller.video_tutorial).replace("client/static/","")
    
    context = {
        'taller': taller,
        'materiales': materiales,
    }
    return render(req, 'child-taller.html', context)


def see_treasure_search(req):
    

    return render(req, 'child-treasure.html')


def get_random_tile(req):
    # Obtener un azulejo aleatorio que tenga coordenadas
    tiles_with_coords = Azulejo.objects.exclude(latitud__isnull=True).exclude(longitud__isnull=True).exclude(latitud=0).exclude(longitud=0)
    
    if not tiles_with_coords.exists():
        return JsonResponse({'error': 'No hay azulejos con coordenadas'}, status=404)
    
    random_tile = random.choice(tiles_with_coords)
    
    random_tile.imagen = clear_dir(random_tile.imagen)
    
    # Crear un diccionario con los datos necesarios
    tile_data = {
        'id': random_tile.id,
        'titulo': random_tile.titulo,
        'nombre': random_tile.nombre,
        'descripcion': random_tile.descripcion,
        'estilo': random_tile.estilo,
        'estilo_display': random_tile.get_estilo_display(),
        'epoca': random_tile.epoca,
        'ubicacion': random_tile.ubicacion,
        'imagen_principal': random_tile.imagen.url,
        'latitud': str(random_tile.latitud),
        'longitud': str(random_tile.longitud),
    }
    
    return JsonResponse(tile_data)


def see_rompecabezas(req):
    
    return render(req, 'child-rompecabezas.html')


def get_random_tile(req):
    # Obtener un azulejo aleatorio que tenga imagen
    tiles_with_images = Azulejo.objects.exclude(imagen_principal='')
    
    if not tiles_with_images.exists():
        return JsonResponse({'error': 'No hay azulejos con imágenes'}, status=404)
    
    random_tile = random.choice(tiles_with_images)
    
    # Crear un diccionario con los datos necesarios
    tile_data = {
        'id': random_tile.id,
        'titulo': random_tile.titulo,
        'nombre': random_tile.nombre,
        'descripcion': random_tile.descripcion,
        'estilo': random_tile.estilo,
        'estilo_display': random_tile.get_estilo_display(),
        'epoca': random_tile.epoca,
        'ubicacion': random_tile.ubicacion,
        'imagen_principal': clear_dir(random_tile.imagen.url),
        'latitud': str(random_tile.latitud),
        'longitud': str(random_tile.longitud),
    }
    
    return JsonResponse(tile_data)


def see_child_librery(req):
    # Filtros
    tipo = req.GET.get('tipo')
    area = req.GET.get('area')
    busqueda = req.GET.get('q')
    
    recursos = RecursoBibliografico.objects.all()
    
    if tipo:
        recursos = recursos.filter(tipo=tipo)
    if area:
        recursos = recursos.filter(area=area)
    if busqueda:
        recursos = recursos.filter(
            models.Q(titulo__icontains=busqueda) |
            models.Q(autor__icontains=busqueda) |
            models.Q(descripcion__icontains=busqueda)
        )
    
    for recurso in recursos:
        recurso.archivo = str(recurso.archivo).replace('client/static/', '')
        recurso.vista_previa = str(recurso.vista_previa).replace('client/static/', '')
    
    # Paginación
    paginator = Paginator(recursos, 12)
    page_number = req.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    
    context = {
        'page_obj': page_obj,
        'tipos': RecursoBibliografico.TIPO_CHOICES,
        'areas': RecursoBibliografico.AREA_CHOICES,
        'filtro_tipo': tipo,
        'filtro_area': area,
        'busqueda': busqueda or '',
    }
    return render(req, 'child-bibliografia.html', context)


def see_child_faders(req):
    
    return render(req, "child-faders.html")

def see_contacto(req):
    if req.method == 'POST':
        name = req.POST.get('name')
        email = req.POST.get('email')
        subject = req.POST.get('subject')
        message = req.POST.get('message')
    
    #     template = render_to_string("emails/admin_contact_email.html", {
    #         'name': name,
    #         'email': email,
    #         'subject': subject,
    #         'message': message,
    #     })
    
    
    #     email = EmailMessage(
    #         subject,
    #         template,
    #         settings.EMAIL_HOST_USER,
    #         ['n62707291@gmail.com']
    #     )
        
        
    #     email.fail_silently = False
    #     email.send()
        
    #     messages.success(req, "Se ha enviado tu correo correctamente. (:")
    #     return redirect("/contacto")
    
    # return render(req, 'contacto.html')
        
        # Validación básica
        if not all([name, email, subject, message]):
            messages.error(req, 'Por favor complete todos los campos del formulario.')
            return redirect('contacto')
    
        try:
            # Enviar correo a los superusuarios
            admin_subject = f"Nuevo mensaje de contacto: {subject}"
            admin_message = f"""
            Nombre: {name}
            Email: {email}
            Asunto: {subject}
        
            Mensaje:
            {message}
            
            ---
            Este mensaje fue enviado desde el formulario de contacto de Azulejos Habaneros.
            """
            
            mail_admins(
                subject=admin_subject,
                message=strip_tags(admin_message),
                html_message=render_to_string('emails/admin_contact_email.html', {
                    'name': name,
                    'email': email,
                    'subject': subject,
                    'message': message,
                }),
                fail_silently=False
            )
            
            # Enviar copia al usuario (opcional)
            user_subject = "Gracias por contactarnos"
            user_message = f"""
            Hola {name},
            
            Hemos recibido tu mensaje con el asunto "{subject}".
            Nuestro equipo te responderá a la brevedad posible.
            
            Este es el mensaje que nos enviaste:
            {message}
            
            Atentamente,
            Equipo de Azulejos Habaneros
            """
            
            send_mail(
                subject=user_subject,
                message=strip_tags(user_message),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                html_message=render_to_string('emails/user_contact_email.html', {
                    'name': name,
                    'subject': subject,
                    'message': message,
                }),
                fail_silently=True
            )
            
            messages.success(req, 'Tu mensaje ha sido enviado con éxito. Te responderemos a la brevedad.')
            return redirect('/contacto')
            
        except Exception as e:
            messages.error(req, f'Ocurrió un error al enviar tu mensaje. Por favor intenta nuevamente. Error: {str(e)}')
            return redirect('/contacto')
    
    return render(req, 'contacto.html')