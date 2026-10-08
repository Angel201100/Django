from django.urls import path
from . import views

urlpatterns = [
    path("", views.crear),
    path("lista/", views.listar),
    path("detalle/<int:id>/", views.detalle),
    path("editar/<int:id>/",views.editar)
]