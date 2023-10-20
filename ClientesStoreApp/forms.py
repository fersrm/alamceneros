from django import forms
from .models import Cliente, Comuna
from .choices import tipoGiro

# --------------------Tabla Usuario ----------


class BaseClienteForm(forms.ModelForm):

  run_cliente = forms.CharField(
      label='Run',
      widget=forms.TextInput(attrs={'class': 'form-control'})
  )
  nombre_cliente = forms.CharField(
      label='Nombre',
      widget=forms.TextInput(attrs={'class': 'form-control'})
  )
  apellido_cliente = forms.CharField(
      label='Apellido',
      widget=forms.TextInput(attrs={'class': 'form-control'})
  )
  correo_cliente = forms.CharField(
      label='Email',
      widget=forms.EmailInput(attrs={'class': 'form-control'})
  )
  razon_social = forms.CharField(
      label='Razon social',
      widget=forms.TextInput(attrs={'class': 'form-control'})
  )
  direccion = forms.CharField(
      label='Direccion',
      widget=forms.TextInput(attrs={'class': 'form-control'})
  )
  comuna_FK = forms.ModelChoiceField(
      label='Comuna',
      queryset=Comuna.objects.all(),
      widget=forms.Select(attrs={'class': 'form-select w-100'})
  )
  tipo_giro = forms.ChoiceField(
      label='Tipo de Giro',
      choices=tipoGiro,
      widget=forms.Select(attrs={'class': 'form-select w-100'})
  )

  class Meta:
    model = Cliente
    fields = [
        'run_cliente',
        'nombre_cliente',
        'apellido_cliente',
        'correo_cliente',
        'razon_social',
        'direccion',
        'tipo_giro',
        'comuna_FK'
    ]

  def clean(self):
    cleaned_data = super().clean()
    run_cliente = cleaned_data.get('run_cliente')

    if run_cliente:
      cleaned_data['run_cliente'] = run_cliente.upper()

    return cleaned_data


class ClienteEditarForm(BaseClienteForm):

  class Meta(BaseClienteForm.Meta):
    fields = BaseClienteForm.Meta.fields


class ClienteAgregarForm(BaseClienteForm):

  class Meta(BaseClienteForm.Meta):
    fields = BaseClienteForm.Meta.fields
