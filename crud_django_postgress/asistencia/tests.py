from datetime import date

from django.test import TestCase
from django.urls import reverse

from .models import Asistencia

DATOS = {
    "tipo_documento": "CC",
    "documento": "1020304050",
    "nombres": "Ana María",
    "apellidos": "Pérez Gómez",
    "whatsapp": "3001234567",
    "fecha": "2026-10-07",
    "asistio": "on",
}


class CrudAsistenciaTests(TestCase):
    def crear_registro(self, **extra):
        datos = {"tipo_documento": "CC", "documento": "111", "nombres": "Luis", "apellidos": "Ruiz",
                 "whatsapp": "3000000000", "fecha": date(2026, 10, 7), "asistio": False}
        datos.update(extra)
        return Asistencia.objects.create(**datos)

    def test_crear(self):
        r = self.client.post(reverse("asistencia:crear"), DATOS)
        self.assertRedirects(r, reverse("asistencia:lista"))
        a = Asistencia.objects.get()
        self.assertTrue(a.asistio)
        self.assertEqual(a.fecha, date(2026, 10, 7))

    def test_checkbox_sin_marcar_es_false(self):
        datos = {k: v for k, v in DATOS.items() if k != "asistio"}
        self.client.post(reverse("asistencia:crear"), datos)
        self.assertFalse(Asistencia.objects.get().asistio)

    def test_no_duplica_documento_en_misma_fecha(self):
        self.client.post(reverse("asistencia:crear"), DATOS)
        r = self.client.post(reverse("asistencia:crear"), DATOS)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(Asistencia.objects.count(), 1)

    def test_whatsapp_invalido(self):
        r = self.client.post(reverse("asistencia:crear"), {**DATOS, "whatsapp": "abc"})
        self.assertEqual(Asistencia.objects.count(), 0)
        self.assertContains(r, "solo números")

    def test_listar_y_buscar(self):
        self.crear_registro()
        self.crear_registro(documento="222", nombres="Marta")
        r = self.client.get(reverse("asistencia:lista"), {"q": "Marta"})
        self.assertContains(r, "Marta")
        self.assertNotContains(r, "Luis")

    def test_detalle_404(self):
        self.assertEqual(self.client.get(reverse("asistencia:detalle", args=[999])).status_code, 404)

    def test_editar(self):
        a = self.crear_registro()
        r = self.client.post(reverse("asistencia:editar", args=[a.id]), {**DATOS, "nombres": "Nuevo"})
        self.assertRedirects(r, reverse("asistencia:detalle", args=[a.id]))
        a.refresh_from_db()
        self.assertEqual(a.nombres, "Nuevo")

    def test_alternar(self):
        a = self.crear_registro()
        self.client.post(reverse("asistencia:alternar", args=[a.id]))
        a.refresh_from_db()
        self.assertTrue(a.asistio)

    def test_eliminar_requiere_post(self):
        a = self.crear_registro()
        self.client.get(reverse("asistencia:eliminar", args=[a.id]))
        self.assertEqual(Asistencia.objects.count(), 1)
        self.client.post(reverse("asistencia:eliminar", args=[a.id]))
        self.assertEqual(Asistencia.objects.count(), 0)
