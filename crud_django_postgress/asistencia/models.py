import datetime

from django.db import models


class Asistencia(models.Model):
    TIPOS_DOCUMENTO = [
        ("CC", "Cédula de ciudadanía"),
        ("TI", "Tarjeta de identidad"),
        ("CE", "Cédula de extranjería"),
        ("PPT", "Permiso por protección temporal"),
        ("PA", "Pasaporte"),
    ]

    # El campo id (BigAutoField) lo crea Django automáticamente.
    tipo_documento = models.CharField(max_length=3, choices=TIPOS_DOCUMENTO, default="CC")
    documento = models.CharField(max_length=20)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    whatsapp = models.CharField(max_length=20)
    fecha = models.DateField(default=datetime.date.today)
    asistio = models.BooleanField(default=False)

    class Meta:
        ordering = ["-fecha", "apellidos", "nombres"]
        constraints = [
            # Una persona solo puede tener un registro por día.
            models.UniqueConstraint(
                fields=["documento", "fecha"],
                name="unico_documento_por_fecha",
                violation_error_message="Ya existe un registro de asistencia para este documento en esa fecha.",
            )
        ]

    def __str__(self):
        return f"{self.nombres} {self.apellidos} - {self.fecha}"
