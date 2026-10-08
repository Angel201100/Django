from django import forms

from .models import Asistencia


class AsistenciaForm(forms.ModelForm):
    class Meta:
        model = Asistencia
        fields = ["tipo_documento", "documento", "nombres", "apellidos", "whatsapp", "fecha", "asistio"]
        widgets = {
            "fecha": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "whatsapp": forms.TextInput(attrs={"placeholder": "3001234567", "inputmode": "tel"}),
            "documento": forms.TextInput(attrs={"inputmode": "numeric"}),
        }
        labels = {
            "tipo_documento": "Tipo de documento",
            "asistio": "¿Asistió?",
        }

    def clean_documento(self):
        return self.cleaned_data["documento"].strip()

    def clean_whatsapp(self):
        valor = self.cleaned_data["whatsapp"].strip().replace(" ", "")
        if not valor.lstrip("+").isdigit():
            raise forms.ValidationError("Ingresa solo números (puede iniciar con +).")
        return valor
