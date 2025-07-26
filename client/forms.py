from django import forms
from .models import Azulejo, RecursoBibliografico, MiembroEquipo, CuentoAnimado, TallerCreativo
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class AzulejoForm(forms.ModelForm):
    required_css_class = 'required-field'
    
    class Meta:
        model = Azulejo
        fields = '__all__'
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'estilo': forms.Select(attrs={'class': 'form-select'}),
            'epoca': forms.TextInput(attrs={'class': 'form-control'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control'}),
            'imagen_principal': forms.FileInput(attrs={'class': 'form-control'}),
            'imagen_detalle': forms.FileInput(attrs={'class': 'form-control'}),
            'coleccion': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'imagen_principal': 'Imagen principal (Recomendado 800x600)',
            'imagen_detalle': 'Imagen detalle (Opcional)',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.widget.attrs['placeholder'] = 'Requerido'
                field.label = f"{field.label} *"

class RecursoForm(forms.ModelForm):
    required_css_class = 'required-field'
    
    class Meta:
        model = RecursoBibliografico
        fields = '__all__'
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'area': forms.Select(attrs={'class': 'form-select'}),
            'autor': forms.TextInput(attrs={'class': 'form-control'}),
            'archivo': forms.FileInput(attrs={'class': 'form-control'}),
            'vista_previa': forms.FileInput(attrs={'class': 'form-control'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_publicacion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.required:
                field.widget.attrs['placeholder'] = 'Requerido'
                field.label = f"{field.label} *"

class MiembroForm(forms.ModelForm):
    class Meta:
        model = MiembroEquipo
        fields = '__all__'
        widgets = {
            'biografia': forms.Textarea(attrs={'rows': 3}),
            'proyectos_destacados': forms.Textarea(attrs={'rows': 3}),
            'imagen': forms.FileInput(attrs={'accept': 'image/*'}),
        }

class CuentoForm(forms.ModelForm):
    class Meta:
        model = CuentoAnimado
        fields = '__all__'
        widgets = {
            'contenido': forms.Textarea(attrs={'rows': 5}),
            'descripcion': forms.Textarea(attrs={'rows': 3}),
            'portada': forms.FileInput(attrs={'accept': 'image/*'}),
            'archivo_animado': forms.FileInput(),
        }

class TallerForm(forms.ModelForm):
    class Meta:
        model = TallerCreativo
        fields = '__all__'
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
            'materiales_necesarios': forms.Textarea(attrs={'rows': 3}),
            'imagen_portada': forms.FileInput(attrs={'accept': 'image/*'}),
            'video_tutorial': forms.FileInput(),
        }

class ThemeForm(forms.Form):
    THEME_CHOICES = [
        ('light', 'Claro'),
        ('dark', 'Oscuro'),
        ('system', 'Sistema'),
    ]
    theme = forms.ChoiceField(
        choices=THEME_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'btn-check'}),
        label="Tema de la interfaz"
    )


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Eliminamos el campo de contraseña que viene por defecto
        self.fields.pop('password', None)
        # Personalizamos los campos si es necesario
        self.fields['username'].help_text = None


class UsuarioForm(UserChangeForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Dejar vacío para no cambiar',
            'autocomplete': 'new-password'
        }),
        required=False,
        strip=False,
        help_text=""
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 
                'password', 'is_active', 'is_staff', 'is_superuser', 'groups')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['groups'].widget.attrs.update({'class': 'form-select'})
        
        if self.instance.pk:
            self.fields['password'].help_text = "Dejar en blanco para mantener la contraseña actual"