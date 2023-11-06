from django import forms
from .models import Proveedor, Giro, Rubro


class BaseProveedorForm(forms.ModelForm):

  run_proveedor = forms.CharField(
      label='RUT',
      widget=forms.TextInput(attrs={'class': 'form-control'})
  )
  nombre_proveedor = forms.CharField(
      label='Nombre Empresa',
      widget=forms.TextInput(attrs={'class': 'form-control'})
  )
  razon_social = forms.CharField(
      label='Razaon social',
      widget=forms.TextInput(attrs={'class': 'form-control'})
  )
  correo_proveedor = forms.CharField(
      label='Email',
      widget=forms.EmailInput(attrs={'class': 'form-control'})
  )
  telefono_proveedor = forms.CharField(
      label='Telefono',
      widget=forms.TextInput(attrs={'class': 'form-control'})
  )
  direccion = forms.CharField(
      label='Direccion',
      widget=forms.TextInput(attrs={'class': 'form-control'})
  )
  contacto = forms.CharField(
      label='Contacto',
      widget=forms.TextInput(attrs={'class': 'form-control'})
  )

  giro_FK = forms.ModelChoiceField(
      label='Giro',
      queryset=Giro.objects.all(),
      widget=forms.Select(attrs={'class': 'form-select'})
  )

  rubro_FK = forms.ModelChoiceField(
      label='Categoria',
      queryset=Rubro.objects.all(),
      widget=forms.Select(attrs={'class': 'form-select'})
  )

  class Meta:
    model = Proveedor
    fields = [
        'run_proveedor',
        'nombre_proveedor',
        'razon_social',
        'correo_proveedor',
        'telefono_proveedor',
        'contacto',
        'direccion',
        'giro_FK',
        'rubro_FK',
    ]

  def clean(self):
    cleaned_data = super().clean()
    run_proveedor = cleaned_data.get('run_proveedor')

    if run_proveedor:
      cleaned_data['run_proveedor'] = run_proveedor.upper()

    return cleaned_data


class ProveedorEditarForm(BaseProveedorForm):

  class Meta(BaseProveedorForm.Meta):
    fields = BaseProveedorForm.Meta.fields


class ProveedorAgregarForm(BaseProveedorForm):

  class Meta(BaseProveedorForm.Meta):
    fields = BaseProveedorForm.Meta.fields
