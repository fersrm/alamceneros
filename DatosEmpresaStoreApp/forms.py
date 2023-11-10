from django import forms
from .models import DatosEmpresa

# -------------------DatosEmpresa----------------


class DatosEmpresaEditarContactoForm(forms.ModelForm):
    telefono = forms.CharField(
        label="Telefono", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    email = forms.CharField(
        label="Email", widget=forms.EmailInput(attrs={"class": "form-control"})
    )
    minimo_boleta = forms.CharField(
        label="Minimo Boletas",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = DatosEmpresa
        fields = ["telefono", "email", "minimo_boleta"]
