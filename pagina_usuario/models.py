from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    title = models.CharField(max_length=100, verbose_name="Título de la actividad")
    description = models.TextField(blank=True, verbose_name="Detalles")
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False, verbose_name="Es prioritaria")
    archivo = models.FileField(upload_to='tareas/', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Tarea"
        verbose_name_plural = "Lista de Tareas"
        ordering = ['-created']

    def __str__(self):
        return f"{self.title} | {self.user.username}"

class DatosPersonales(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Usuario Asociado")
    foto = models.ImageField(upload_to='perfil/', null=True, blank=True, verbose_name="Fotografía")
    nombres = models.CharField(max_length=60, verbose_name="Nombres Completos")
    apellidos = models.CharField(max_length=60)
    cedula = models.CharField(max_length=10, unique=True, verbose_name="Documento de Identidad")
    nacionalidad = models.CharField(max_length=20)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    direccion_domiciliaria = models.CharField(max_length=100, verbose_name="Dirección")
    perfil_profesional = models.TextField(max_length=500, verbose_name="Resumen Profesional")

    class Meta:
        verbose_name = "Expediente Personal"
        verbose_name_plural = "Expedientes"

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

class ExperienciaLaboral(models.Model):
    perfil = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE, related_name='experiencias')
    nombre_empresa = models.CharField(max_length=100, verbose_name="Empresa")
    cargo_desempenado = models.CharField(max_length=100, verbose_name="Cargo")
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True, verbose_name="Fecha Fin (Dejar vacío si es actual)")

    class Meta:
        verbose_name = "Experiencia"
        verbose_name_plural = "Trayectoria Laboral"

class Curso(models.Model):
    perfil = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE, related_name='cursos')
    nombre_curso = models.CharField(max_length=100)
    institucion = models.CharField(max_length=100)
    horas = models.IntegerField(verbose_name="Duración (Horas)")

    class Meta:
        verbose_name = "Certificación"
        verbose_name_plural = "Cursos y Certificaciones"

class ProductoLaboral(models.Model):
    perfil = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE, related_name='productos_lab')
    nombre_producto = models.CharField(max_length=100, verbose_name="Nombre del Proyecto")
    descripcion = models.CharField(max_length=200)

class ProductoAcademico(models.Model):
    perfil = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE, related_name='productos_acad')
    nombre_recurso = models.CharField(max_length=100, verbose_name="Título del Recurso")
    descripcion = models.CharField(max_length=200)

class Recomendacion(models.Model):
    perfil = models.ForeignKey(DatosPersonales, on_delete=models.CASCADE, related_name='recomendaciones')
    nombre_persona = models.CharField(max_length=100, verbose_name="Referencia")
    telefono = models.CharField(max_length=15, verbose_name="Contacto")
    