from django.contrib import admin
from .models import (
    DatosPersonales, ExperienciaLaboral, Curso, 
    ProductoLaboral, ProductoAcademico, Recomendacion
)

# ==========================================================
# 1. IDENTIDAD CORPORATIVA PROGRESSUS
# ==========================================================
admin.site.site_header = "Plataforma PROGRESSUS"
admin.site.site_title = "Admin Progressus"
admin.site.index_title = "Gestión Centralizada del Sistema"
admin.site.site_url = '/' 

# ==========================================================
# 2. CONFIGURACIÓN DE PESTAÑAS (INLINES)
# ==========================================================
class ExperienciaInline(admin.TabularInline):
    model = ExperienciaLaboral
    extra = 0 # No mostrar filas vacías innecesarias
    classes = ('collapse',) # Permite contraer la sección para limpieza visual
    verbose_name = "Experiencia Laboral"
    verbose_name_plural = "Historial Laboral"

class CursoInline(admin.TabularInline):
    model = Curso
    extra = 0
    classes = ('collapse',)
    verbose_name = "Formación / Curso"
    verbose_name_plural = "Formación Académica"

class RecomendacionInline(admin.TabularInline):
    model = Recomendacion
    extra = 0
    verbose_name = "Referencia"
    verbose_name_plural = "Referencias Personales"

class ProductoLaboralInline(admin.TabularInline):
    model = ProductoLaboral
    extra = 0
    verbose_name = "Proyecto Laboral"
    verbose_name_plural = "Portafolio Laboral"

class ProductoAcademicoInline(admin.TabularInline):
    model = ProductoAcademico
    extra = 0
    verbose_name = "Logro Académico"
    verbose_name_plural = "Portafolio Académico"

# ==========================================================
# 3. ADMINISTRACIÓN DE PERFILES
# ==========================================================

@admin.register(DatosPersonales)
class DatosPersonalesAdmin(admin.ModelAdmin):
    # Columnas que se ven en la lista principal
    list_display = ('nombres', 'apellidos', 'cedula', 'nacionalidad_display')
    search_fields = ('nombres', 'apellidos', 'cedula')
    list_filter = ('nacionalidad',)
    
    # Organización visual dentro del formulario
    fieldsets = (
        ('Información Principal', {
            'fields': (('nombres', 'apellidos'), 'cedula', 'user', 'foto')
        }),
        ('Detalles Personales', {
            'fields': ('fecha_nacimiento', 'nacionalidad', 'direccion_domiciliaria'),
            'classes': ('collapse',)
        }),
        ('Perfil Profesional', {
            'fields': ('perfil_profesional',)
        }),
    )

    inlines = [
        ExperienciaInline, 
        CursoInline, 
        ProductoLaboralInline, 
        ProductoAcademicoInline, 
        RecomendacionInline
    ]

    def nacionalidad_display(self, obj):
        return obj.nacionalidad.upper()
    nacionalidad_display.short_description = 'País de Origen'

# Registros individuales (Opcional, si quieres gestionarlos fuera del perfil)
admin.site.register(ExperienciaLaboral)
admin.site.register(Curso)