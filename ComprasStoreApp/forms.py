from django import forms
from .models import Compras, Proveedor
from .choices import tipoImpuesto, tipoDoc

# --------------------Tabla Usuario ----------


class BaseComprasForm(forms.ModelForm):
    num_documento = forms.CharField(
        label="Número de Documento",
        widget=forms.TextInput(attrs={"class": "form-control", "id": "num_documento"}),
    )
    fecha = forms.DateField(
        label="Fecha",
        widget=forms.DateInput(attrs={"class": "form-control", "id": "fecha"}),
    )
    total = forms.CharField(
        label="Total",
        widget=forms.NumberInput(attrs={"class": "form-control", "id": "total"}),
    )
    tipo_documento = forms.ChoiceField(
        label="Tipo de Documento",
        choices=tipoDoc,
        widget=forms.Select(attrs={"class": "form-select", "id": "tipo_documento"}),
    )
    tipo_impuesto = forms.ChoiceField(
        label="Con/Sin Impuesto",
        choices=tipoImpuesto,
        widget=forms.Select(attrs={"class": "form-select", "id": "tipo_impuesto"}),
    )
    proveedor_FK = forms.ModelChoiceField(
        label="Proveedor",
        queryset=Proveedor.objects.all(),
        widget=forms.Select(attrs={"class": "form-select", "id": "proveedor"}),
    )

    class Meta:
        model = Compras
        fields = [
            "num_documento",
            "fecha",
            "total",
            "tipo_documento",
            "tipo_impuesto",
            "proveedor_FK",
        ]

    def clean(self):
        cleaned_data = super().clean()
        num_documento = cleaned_data.get("num_documento")

        if num_documento:
            cleaned_data["num_documento"] = num_documento.upper()

        return cleaned_data


class ComprasAgregarForm(BaseComprasForm):
    class Meta(BaseComprasForm.Meta):
        fields = BaseComprasForm.Meta.fields

    # def __init__(self, *args, **kwargs):
    #     super(ComprasAgregarForm, self).__init__(*args, **kwargs)
    #     self.fields["total"].initial = 0
