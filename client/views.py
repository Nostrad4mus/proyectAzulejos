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


from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from .models import Azulejo, RecursoBibliografico, MiembroEquipo, CuentoAnimado, TallerCreativo

@staff_member_required(login_url='/admin/login/')
def admin_dashboard(request):
    context = {
        'azulejos_count': Azulejo.objects.count(),
        'recursos_count': RecursoBibliografico.objects.count(),
        'miembros_count': MiembroEquipo.objects.count(),
        'cuentos_count': CuentoAnimado.objects.count(),
        'talleres_count': TallerCreativo.objects.count(),
    }
    return render(request, 'admin/dashboard.html', context)



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from .models import Azulejo
from .forms import AzulejoForm


@staff_member_required(login_url='/admin/login/')
def admin_dashboard(request):
    context = {
        'azulejos_count': Azulejo.objects.count(),
        'recursos_count': RecursoBibliografico.objects.count(),
        'miembros_count': MiembroEquipo.objects.count(),
        'cuentos_count': CuentoAnimado.objects.count(),
        'talleres_count': TallerCreativo.objects.count(),
    }
    return render(request, 'admin/dashboard.html', context)

@staff_member_required(login_url='/admin/login/')
def admin_azulejos(request):
    # Filtros
    estilo = request.GET.get('estilo')
    busqueda = request.GET.get('q')
    
    azulejos = Azulejo.objects.all()
    
    if estilo:
        azulejos = azulejos.filter(estilo=estilo)
    if busqueda:
        azulejos = azulejos.filter(titulo__icontains=busqueda)
    
    # Ordenación
    orden = request.GET.get('orden', 'titulo')
    azulejos = azulejos.order_by(orden)
    
    context = {
        'azulejos': azulejos,
        'estilos': Azulejo.ESTILOS,
        'orden_actual': orden,
        'form': AzulejoForm()  # Formulario para el modal de creación
    }
    return render(request, 'admin/azulejos.html', context)


@staff_member_required
def crear_azulejo(request):
    if request.method == 'POST':
        form = AzulejoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'errors': 'Método no permitido'})

@staff_member_required
def editar_azulejo(request, pk):
    azulejo = get_object_or_404(Azulejo, pk=pk)
    if request.method == 'POST':
        form = AzulejoForm(request.POST, request.FILES, instance=azulejo)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    
    # Para GET, devolvemos el formulario rellenado
    form = AzulejoForm(instance=azulejo)
    return render(request, 'admin/partials/azulejo_form.html', {'form': form})

@staff_member_required
def eliminar_azulejo(request, pk):
    azulejo = get_object_or_404(Azulejo, pk=pk)
    if request.method == 'POST':
        azulejo.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@staff_member_required
def eliminar_azulejos_multiples(request):
    if request.method == 'POST':
        ids = request.POST.getlist('ids[]')
        Azulejo.objects.filter(id__in=ids).delete()
        return JsonResponse({'success': True, 'count': len(ids)})
    return JsonResponse({'success': False})



from .models import RecursoBibliografico
from .forms import RecursoForm

@staff_member_required
def admin_recursos(request):
    # Filtros
    tipo = request.GET.get('tipo')
    area = request.GET.get('area')
    busqueda = request.GET.get('q')
    
    recursos = RecursoBibliografico.objects.all()
    
    if tipo:
        recursos = recursos.filter(tipo=tipo)
    if area:
        recursos = recursos.filter(area=area)
    if busqueda:
        recursos = recursos.filter(titulo__icontains=busqueda)
    
    # Ordenación
    orden = request.GET.get('orden', '-fecha_subida')
    recursos = recursos.order_by(orden)
    
    context = {
        'recursos': recursos,
        'tipos': RecursoBibliografico.TIPO_CHOICES,
        'areas': RecursoBibliografico.AREA_CHOICES,
        'orden_actual': orden,
        'form': RecursoForm()  # Formulario para el modal de creación
    }
    return render(request, 'admin/recursos.html', context)

@staff_member_required
def crear_recurso(request):
    if request.method == 'POST':
        form = RecursoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False, 'errors': 'Método no permitido'})

@staff_member_required
def editar_recurso(request, pk):
    recurso = get_object_or_404(RecursoBibliografico, pk=pk)
    if request.method == 'POST':
        form = RecursoForm(request.POST, request.FILES, instance=recurso)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    
    form = RecursoForm(instance=recurso)
    return render(request, 'admin/partials/recurso_form.html', {'form': form})

@staff_member_required
def eliminar_recurso(request, pk):
    recurso = get_object_or_404(RecursoBibliografico, pk=pk)
    if request.method == 'POST':
        recurso.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@staff_member_required
def eliminar_recursos_multiples(request):
    if request.method == 'POST':
        ids = request.POST.getlist('ids[]')
        RecursoBibliografico.objects.filter(id__in=ids).delete()
        return JsonResponse({'success': True, 'count': len(ids)})
    return JsonResponse({'success': False})





from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from .models import Azulejo
from .forms import AzulejoForm

@staff_member_required
def editar_azulejo(request, pk):
    azulejo = get_object_or_404(Azulejo, pk=pk)
    if request.method == 'POST':
        form = AzulejoForm(request.POST, request.FILES, instance=azulejo)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})
    
    form = AzulejoForm(instance=azulejo)
    return render(request, 'admin/partials/azulejo_form.html', {'form': form})

@staff_member_required
def eliminar_azulejo(request, pk):
    azulejo = get_object_or_404(Azulejo, pk=pk)
    if request.method == 'POST':
        azulejo.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

@staff_member_required
def eliminar_azulejos_multiples(request):
    if request.method == 'POST':
        ids = request.POST.getlist('ids[]')
        Azulejo.objects.filter(id__in=ids).delete()
        return JsonResponse({'success': True, 'deleted': len(ids)})
    return JsonResponse({'success': False})






from .models import RecursoBibliografico
from .forms import RecursoForm

@staff_member_required
def editar_recurso(request, pk):
    recurso = get_object_or_404(RecursoBibliografico, pk=pk)
    if request.method == 'POST':
        form = RecursoForm(request.POST, request.FILES, instance=recurso)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})
    
    form = RecursoForm(instance=recurso)
    return render(request, 'admin/partials/recurso_form.html', {'form': form})

@staff_member_required
def eliminar_recurso(request, pk):
    recurso = get_object_or_404(RecursoBibliografico, pk=pk)
    if request.method == 'POST':
        recurso.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

@staff_member_required
def eliminar_recursos_multiples(request):
    if request.method == 'POST':
        ids = request.POST.getlist('ids[]')
        RecursoBibliografico.objects.filter(id__in=ids).delete()
        return JsonResponse({'success': True, 'deleted': len(ids)})
    return JsonResponse({'success': False})







from .models import MiembroEquipo, CuentoAnimado, TallerCreativo
from .forms import MiembroForm, CuentoForm, TallerForm

# ---- Miembros del Equipo ----
@staff_member_required
def admin_miembros(request):
    miembros = MiembroEquipo.objects.all().order_by('orden')
    context = {
        'miembros': miembros,
        'roles': MiembroEquipo.ROL_CHOICES,
        'form': MiembroForm()
    }
    return render(request, 'admin/miembros.html', context)

@staff_member_required
def crear_miembro(request):
    if request.method == 'POST':
        form = MiembroForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False})

@staff_member_required
def editar_miembro(request, pk):
    miembro = get_object_or_404(MiembroEquipo, pk=pk)
    if request.method == 'POST':
        form = MiembroForm(request.POST, request.FILES, instance=miembro)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})
    
    form = MiembroForm(instance=miembro)
    return render(request, 'admin/partials/miembro_form.html', {'form': form})

@staff_member_required
def eliminar_miembro(request, pk):
    miembro = get_object_or_404(MiembroEquipo, pk=pk)
    if request.method == 'POST':
        miembro.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

# ---- Cuentos Animados ----
@staff_member_required
def admin_cuentos(request):
    cuentos = CuentoAnimado.objects.all().order_by('-fecha_publicacion')
    context = {
        'cuentos': cuentos,
        'niveles': CuentoAnimado.NIVEL_CHOICES,
        'form': CuentoForm()
    }
    return render(request, 'admin/cuentos.html', context)

@staff_member_required
def crear_cuento(request):
    if request.method == 'POST':
        form = CuentoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False})

@staff_member_required
def editar_cuento(request, pk):
    cuento = get_object_or_404(CuentoAnimado, pk=pk)
    if request.method == 'POST':
        form = CuentoForm(request.POST, request.FILES, instance=cuento)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})
    
    form = CuentoForm(instance=cuento)
    return render(request, 'admin/partials/cuento_form.html', {'form': form})

@staff_member_required
def eliminar_cuento(request, pk):
    cuento = get_object_or_404(CuentoAnimado, pk=pk)
    if request.method == 'POST':
        cuento.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

# ---- Talleres Creativos ----
@staff_member_required
def admin_talleres(request):
    talleres = TallerCreativo.objects.all().order_by('-fecha_publicacion')
    context = {
        'talleres': talleres,
        'niveles': TallerCreativo.NIVEL_DIFICULTAD,
        'tipos': TallerCreativo.TIPO_TALLER,
        'form': TallerForm()
    }
    return render(request, 'admin/talleres.html', context)

@staff_member_required
def crear_taller(request):
    if request.method == 'POST':
        form = TallerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})
    return JsonResponse({'success': False})

@staff_member_required
def editar_taller(request, pk):
    taller = get_object_or_404(TallerCreativo, pk=pk)
    if request.method == 'POST':
        form = TallerForm(request.POST, request.FILES, instance=taller)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors})
    
    form = TallerForm(instance=taller)
    return render(request, 'admin/partials/taller_form.html', {'form': form})

@staff_member_required
def eliminar_taller(request, pk):
    taller = get_object_or_404(TallerCreativo, pk=pk)
    if request.method == 'POST':
        taller.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})





from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.decorators import login_required

from .forms import CustomUserChangeForm

@staff_member_required
def perfil_usuario(request):
    user = request.user
    if request.method == 'POST':
        # Usamos una versión personalizada del formulario
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado correctamente')
            return redirect('perfil_usuario')
    else:
        # Creamos una instancia del formulario personalizado
        form = CustomUserChangeForm(instance=user)
    
    context = {
        'form': form,
        'user': user
    }
    return render(request, 'admin/perfil.html', context)

from django.http import JsonResponse

@staff_member_required
def configuracion_usuario(request):
    if request.method == 'POST':
        if 'theme' in request.POST:
            form = ThemeForm(request.POST)
            if form.is_valid():
                request.session['theme'] = form.cleaned_data['theme']
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': True})
                messages.success(request, 'Preferencias guardadas correctamente')
                return redirect('configuracion_usuario')
        
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Contraseña cambiada correctamente')
            return redirect('configuracion_usuario')
    else:
        form = PasswordChangeForm(request.user)
    
    theme_form = ThemeForm(initial={'theme': request.session.get('theme', 'light')})
    
    context = {
        'form': form,
        'theme_form': theme_form
    }
    return render(request, 'admin/configuracion.html', context)


# views.py
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

@require_POST
def custom_logout(request):
    logout(request)
    return redirect('login')  # Cambia 'login' por tu URL de inicio de sesión




# views.py
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

@require_POST
def custom_logout(request):
    logout(request)
    return redirect('login')  # Cambia 'login' por tu URL de inicio de sesión



from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib.auth.forms import AuthenticationForm

class CustomLoginView(SuccessMessageMixin, LoginView):
    template_name = 'admin/login.html'
    form_class = AuthenticationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('admin_dashboard')
    success_message = "Has iniciado sesión correctamente"
    
    def get_success_url(self):
        return self.success_url
    
    def form_invalid(self, form):
        messages.error(self.request, "Credenciales incorrectas. Inténtalo de nuevo.")
        return super().form_invalid(form)

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')
    
    def dispatch(self, request, *args, **kwargs):
        messages.info(request, "Has cerrado sesión correctamente")
        return super().dispatch(request, *args, **kwargs)





from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from .forms import UsuarioForm

User = get_user_model()

def superuser_required(view_func):
    return user_passes_test(
        lambda u: u.is_superuser,
        login_url='admin_dashboard'
    )(view_func)
    
    
@superuser_required
def gestion_usuarios(request):
    usuarios = User.objects.all().order_by('-date_joined')
    form = UsuarioForm()  # Formulario vacío para creación
    
    return render(request, 'admin/gestion_usuarios.html', {
        'usuarios': usuarios,
        'form': form,  # Asegúrate de pasar el formulario
        'total_usuarios': usuarios.count(),
        'staff_count': User.objects.filter(is_staff=True).count(),
    })

@superuser_required
def crear_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Usuario {user.username} creado correctamente')
            return redirect('gestion_usuarios')
    else:
        form = UsuarioForm()
    
    return render(request, 'admin/partials/usuario_form.html', {'form': form})

@superuser_required
def editar_usuario(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        print(request.POST)
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            user = form.save()
            return JsonResponse({
                'success': True,
                'message': f'Usuario {user.username} actualizado'
            })
        
        # Debug: Imprimir errores en consola
        print("Errores del formulario:", form.errors)
        return JsonResponse({
            'success': False,
            'errors': form.errors.get_json_data()
        }, status=400)
    
    form = UsuarioForm(instance=usuario)
    return render(request, 'admin/partials/usuario_form.html', {'form': form})

@superuser_required
def eliminar_usuario(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        username = usuario.username
        usuario.delete()
        messages.success(request, f'Usuario {username} eliminado correctamente')
        return JsonResponse({'success': True, 'message': f'Usuario {username} eliminado'})
    
    return JsonResponse({
        'success': False,
        'error': 'Método no permitido'
    }, status=400)