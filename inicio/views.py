from django.shortcuts import render

# Create your views here.

def inicio(request, *args, **kwargs):
    return render(request, 'inicio/inicio.html')