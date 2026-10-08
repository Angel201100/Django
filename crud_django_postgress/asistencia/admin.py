from django.contrib import admin

from .models import Asistencia


@admin.register(Asistencia)
class AsistenciaAdmin(admin.ModelAdmin):
    list_display = ("documento", "nombres", "apellidos", "whatsapp", "fecha", "asistio")
    list_filter = ("fecha", "asistio", "tipo_documento")
    search_fields = ("documento", "nombres", "apellidos")
