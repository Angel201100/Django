from django.urls import path

from . import views

app_name = "asistencia"

urlpatterns = [
    path("", views.listar, name="lista"),
    path("nuevo/", views.crear, name="crear"),
    path("<int:id>/", views.detalle, name="detalle"),
    path("<int:id>/editar/", views.editar, name="editar"),
    path("<int:id>/eliminar/", views.eliminar, name="eliminar"),
    path("<int:id>/alternar/", views.alternar_asistencia, name="alternar"),
]
