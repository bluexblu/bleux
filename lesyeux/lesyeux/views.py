from django.shortcuts import render

# Vista para la página de inicio de Lesyeux
def inicio(request):
    return render(request, 'lesyeux/inicio.html')

# Vista para la página de contacto
def contacto(request):
    return render(request, 'lesyeux/contacto.html')
