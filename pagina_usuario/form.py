from django import forms
from .models import DatosPersonales

class PerfilForm(forms.ModelForm):
    class Meta:
        model = DatosPersonales
        fields = ['foto', 'nombres', 'apellidos', 'cedula', 'nacionalidad', 'perfil_profesional', 'direccion_domiciliaria']
        
        # Etiquetas amigables para el formulario
        labels = {
            'nombres': 'Tus Nombres',
            'apellidos': 'Tus Apellidos',
            'cedula': 'Documento de Identidad (DNI/Cédula)',
            'perfil_profesional': 'Extracto Profesional (Cuéntanos sobre ti)',
            'foto': 'Fotografía de Perfil'
        }

        # Estilos CSS inyectados directamente al input HTML
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Juan Carlos'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Pérez Gómez'}),
            'cedula': forms.TextInput(attrs={'class': 'form-control'}),
            'nacionalidad': forms.TextInput(attrs={'class': 'form-control'}),
            'perfil_profesional': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Soy un profesional apasionado por...'}),
            'direccion_domiciliaria': forms.TextInput(attrs={'class': 'form-control'}),
            'foto': forms.FileInput(attrs={'class': 'form-control'})
        }