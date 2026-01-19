from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.utils import timezone

# Importación optimizada
from .models import Task, DatosPersonales
from .form import PerfilForm

# ==========================================================
# VISTAS PÚBLICAS (ACCESO Y REGISTRO)
# ==========================================================

def home(request):
    """Página de aterrizaje principal."""
    return render(request, 'home.html')

def signup(request):
    """Gestión de nuevos registros."""
    if request.method == 'GET':
        return render(request, 'signup.html', {'form': UserCreationForm()})
    else:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('tasks')
        else:
            # Mensaje humanizado
            return render(request, 'signup.html', {
                'form': form, 
                'error': 'Algo no salió bien. Verifica que la contraseña sea segura y coincida.'
            })

def signin(request):
    """Inicio de sesión corporativo."""
    if request.method == 'GET':
        return render(request, 'signin.html', {'form': AuthenticationForm()})
    else:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('tasks')
        else:
            # Mensaje humanizado
            return render(request, 'signin.html', {
                'form': form, 
                'error': 'No pudimos acceder. Revisa tus credenciales e inténtalo de nuevo.'
            })

@login_required
def signout(request):
    """Cierre de sesión seguro."""
    logout(request)
    return redirect('home')

# ==========================================================
# VISTAS PRIVADAS (ÁREA DE TRABAJO)
# ==========================================================

@login_required
def tasks(request):
    """Tablero principal de actividades."""
    # Priorizamos las pendientes más recientes
    tasks_pending = Task.objects.filter(user=request.user, datecompleted__isnull=True).order_by('-created')
    tasks_completed = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    
    return render(request, 'task.html', {
        'tasks_pending': tasks_pending, 
        'tasks_completed': tasks_completed
    })

@login_required
def create_task(request):
    """Creación de nuevas asignaciones."""
    if request.method == 'GET':
        return render(request, 'create_tasks.html')
    else:
        title = request.POST.get('title')
        if title:
            Task.objects.create(
                title=title,
                description=request.POST.get('description', ''),
                important='important' in request.POST,
                archivo=request.FILES.get('archivo'),
                user=request.user
            )
            return redirect('tasks')
        
        return render(request, 'create_tasks.html', {
            'error': 'Por favor, escribe al menos un título para saber qué vamos a hacer.'
        })

@login_required
def complete_task(request, task_id):
    """Marcar tarea como finalizada."""
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.datecompleted = timezone.now()
    task.save()
    return redirect('tasks')

# ==========================================================
# GESTIÓN DE PERFIL PROFESIONAL
# ==========================================================

@login_required
def hoja_vida(request):
    """Visualización del expediente profesional."""
    # 'select_related' optimiza la consulta a la base de datos
    datos = DatosPersonales.objects.filter(user=request.user).select_related('user').first()
    return render(request, 'hoja de vida.html', {'perfil': datos})

@login_required
def editar_perfil(request):
    """Edición de datos del usuario."""
    perfil, created = DatosPersonales.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            return redirect('hoja_vida')
    else:
        form = PerfilForm(instance=perfil)
        
    return render(request, 'editar_perfil.html', {'form': form})