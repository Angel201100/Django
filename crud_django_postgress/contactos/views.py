from django.shortcuts import render
from .models import Contacto

# Create your views here.
def crear(request):
    if request.method == "POST":
        contacto = Contacto(
            nombre = request.POST["nombre"],
            correo = request.POST["correo"],
            telefono = request.POST["telefono"],
            mensaje = request.POST["mensaje"]
        )

        contacto.save() #Guardar el contacto
    return render(request, "formulario.html")

#Método para listar los datos del contacto
def listar(request):
    #Traer todos los registros de la tabla contactos. #Select * from contactos
    contactos = Contacto.objects.all()
    return render(
        request,
        "lista.html",
        {"contactos":contactos}
    )

#Consultar la información de un registro
def detalle(request,id):
    contacto = Contacto.objects.get(id=id)#SELECT * FROM Contacto WHERE id=7
    return render(
        request, 
        "detalle.html",
        {"contacto": contacto})

#Editar: Modicar los datos de un registro.
def editar(request, id):
    #Busar el contacto
    contacto = Contacto.objects.get(id=id)#SELECT * FROM Contacto WHERE id=7
    
    if request.method=="POST":#Si se van a guardar los cambios
        contacto.nombre = request.POST["nombre"] #Cambiar el nombre del contacto
        contacto.correo = request.POST["correo"] #Cambiar el correo del contacto
        contacto.telefono = request.POST["telefono"] #Cambiar el telefono del contacto
        contacto.mensaje = request.POST["mensaje"] #Cambiar el mensaje del contacto

        contacto.save() #Guardar los cambios

        return render(
            request,
            "detalle.html",
            {"contacto":contacto}
        )
    
    return render(
        request,
        "formulario.html",
        {"contacto": contacto}
    )

def eliminar(request,id):
    contacto = Contacto.objects.get(id=id)#SELECT * FROM Contacto WHERE id=7
    contacto.delete() #DELETE FROM Contacto WHERE id= 7 Eliminación en SQl
    return render(
            request,
            "detalle.html",
            {"contacto":contacto}
        )

"""Falto 28-09-2026:
Mathias,
Sebastián
Andrés.
Simón.
Emanuel Tangarife
Samuel Mora.
"""
