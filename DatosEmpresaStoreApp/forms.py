from django import forms
from .models import DatosEmpresa

# -------------------DatosEmpresa----------------


class DatosEmpresaEditarContactoForm(forms.ModelForm):
    telefono = forms.CharField(
        label="Teléfono", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    email = forms.EmailField(
        label="Email", widget=forms.EmailInput(attrs={"class": "form-control"})
    )
    minimo_boleta = forms.IntegerField(
        label="Mínimo Boletas",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = DatosEmpresa
        fields = ["telefono", "email", "minimo_boleta"]


class DatosEmpresaEditarForm(forms.ModelForm):
    IVA = forms.IntegerField(
        label="IVA %",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    margen_global = forms.DecimalField(
        label="Margen Global %",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = DatosEmpresa
        fields = ["IVA", "margen_global"]
