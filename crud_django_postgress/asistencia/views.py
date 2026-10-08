from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import AsistenciaForm
from .models import Asistencia


def listar(request):
    """READ (lista): SELECT * FROM asistencia, con búsqueda y filtros opcionales."""
    registros = Asistencia.objects.all()

    q = request.GET.get("q", "").strip()
    fecha = request.GET.get("fecha", "").strip()
    estado = request.GET.get("estado", "")

    if q:
        registros = registros.filter(
            Q(documento__icontains=q) | Q(nombres__icontains=q) | Q(apellidos__icontains=q)
        )
    if fecha:
        registros = registros.filter(fecha=fecha)
    if estado == "si":
        registros = registros.filter(asistio=True)
    elif estado == "no":
        registros = registros.filter(asistio=False)

    return render(
        request,
        "asistencia/lista.html",
        {"registros": registros, "q": q, "fecha": fecha, "estado": estado},
    )


def crear(request):
    """CREATE: INSERT INTO asistencia ..."""
    form = AsistenciaForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Registro creado correctamente.")
        return redirect("asistencia:lista")
    return render(request, "asistencia/formulario.html", {"form": form, "titulo": "Nuevo registro"})


def detalle(request, id):
    """READ (uno): SELECT * FROM asistencia WHERE id = ..."""
    registro = get_object_or_404(Asistencia, id=id)
    return render(request, "asistencia/detalle.html", {"registro": registro})


def editar(request, id):
    """UPDATE: UPDATE asistencia SET ... WHERE id = ..."""
    registro = get_object_or_404(Asistencia, id=id)
    form = AsistenciaForm(request.POST or None, instance=registro)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Registro actualizado correctamente.")
        return redirect("asistencia:detalle", id=registro.id)
    return render(
        request,
        "asistencia/formulario.html",
        {"form": form, "titulo": "Editar registro", "registro": registro},
    )


def eliminar(request, id):
    """DELETE: pide confirmación (GET) y borra solo por POST."""
    registro = get_object_or_404(Asistencia, id=id)
    if request.method == "POST":
        registro.delete()
        messages.success(request, "Registro eliminado.")
        return redirect("asistencia:lista")
    return render(request, "asistencia/confirmar_eliminar.html", {"registro": registro})


@require_POST
def alternar_asistencia(request, id):
    """Marca/desmarca rápidamente la asistencia desde la lista."""
    registro = get_object_or_404(Asistencia, id=id)
    registro.asistio = not registro.asistio
    registro.save(update_fields=["asistio"])
    return redirect("asistencia:lista")
