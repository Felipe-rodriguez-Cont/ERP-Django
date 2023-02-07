from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# importamos el formulario que acabamos de crear en forms.py
from .forms import TaskForm, Task


# Create your views here.
def home(request):
    return render(request, 'home.html')


def registrarse(request):
    if request.method == 'GET':
        print("enviando formulario por get")

        return render(request, 'registrarse.html', {
            'form': UserCreationForm
        })
    else:
        print(request.POST)
        if request.POST['password1'] == request.POST['password2']:
            try:
                # registrar y guardar usuario en la base de datos a prueba de errores con try
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                # autentificamos al usuario con bivlioteca de django login
                login(request, user)
                # redireccionamos a una pagina en caso de que todo no existan errores
                # se debe de colocar el Name de path (guardado en urls.py)
                return redirect('tasks')

            except IntegrityError:  # se llama a integrity dado que la pagina arroja error al tener usuarios repetidos en la bbdd
                return render(request, 'registrarse.html', {
                    'form': UserCreationForm,
                    'error': 'USUARIO YA EXISTE',
                })
        return render(request, 'registrarse.html', {
            'form': UserCreationForm,
            'error': 'LAS CONTRASEÑAS NO SON IGUALES, INTENTALO DE NUEVO PUTITO',
        })

@login_required
def task(request):
    # consulta para que retorne todos los campos de la tabla task en la bbdd
    task = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'task.html', {'task': task})
@login_required
def tasks_completed(request):
    task = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'task.html', {"task": task})


def about(request):
    return render(request, 'about.html')

@login_required
def cerrarSecion(request):
    logout(request)
    return redirect('home')


def signin(request):
    # si los datos arrojados son get, envia el formulario
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        # autentificamos usuarios comprobando si los datos enviados son validos.
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        print(request.POST)
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'usuario o contraseña invalidas'})
        else:
            login(request, user)
            return redirect('tasks')

@login_required
def createTask(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {'form': TaskForm })
    else:
        try:

            # capturamos los datos enviados por post en el formulario y lo guardamos
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            print(new_task)
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {
                'form': TaskForm,
                'error': 'por favor provee datos validos',
            })

@login_required
def task_create(request):
    return (request, 'task_create.html')
@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task':task, 'form':form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {'task':task, 'form':form, 'error':"ERROR ACTUALIZANDO LA TAREA PUTITO"})

@login_required
def complete_task(request, task_id):
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        if request.method == 'POST':
            task.datecompleted = timezone.now()
            task.save()
            return redirect('tasks')
@login_required         
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')
    
