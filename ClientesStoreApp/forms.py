from django import forms
from .models import Cliente

# --------------------Tabla Usuario ----------


class BaseClienteForm(forms.ModelForm):
    run_cliente = forms.CharField(
        label="Run", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    nombre_cliente = forms.CharField(
        label="Nombre", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    apellido_cliente = forms.CharField(
        label="Apellido", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    correo_cliente = forms.CharField(
        label="Email", widget=forms.EmailInput(attrs={"class": "form-control"})
    )
    telefono_cliente = forms.CharField(
        label="Telefono", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    direccion = forms.CharField(
        label="Direccion", widget=forms.TextInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = Cliente
        fields = [
            "run_cliente",
            "nombre_cliente",
            "apellido_cliente",
            "correo_cliente",
            "telefono_cliente",
            "direccion",
        ]

    def clean(self):
        cleaned_data = super().clean()
        run_cliente = cleaned_data.get("run_cliente")

        if run_cliente:
            cleaned_data["run_cliente"] = run_cliente.upper()

        return cleaned_data


class ClienteEditarForm(BaseClienteForm):
    class Meta(BaseClienteForm.Meta):
        fields = BaseClienteForm.Meta.fields


class ClienteAgregarForm(BaseClienteForm):
    class Meta(BaseClienteForm.Meta):
        fields = BaseClienteForm.Meta.fields
