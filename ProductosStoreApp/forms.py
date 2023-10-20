from django import forms
from .models import Producto, Marca, Categoria

# -------------------------Productos--------------


class BaseProductoForm(forms.ModelForm):

  nombre_producto = forms.CharField(
      label='Nombre del producto',
      widget=forms.TextInput(attrs={'class': 'form-control'})
  )
  precio_producto = forms.DecimalField(
      label='Precio del producto',
      widget=forms.NumberInput(attrs={'class': 'form-control'})
  )
  imagen = forms.ImageField(
      label='Imagen',
      widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
  )
  stock = forms.DecimalField(
      label='Stock del producto',
      widget=forms.NumberInput(attrs={'class': 'form-control'})
  )
  marca_FK = forms.ModelChoiceField(
      label='Marca',
      queryset=Marca.objects.all(),
      widget=forms.Select(attrs={'class': 'form-select w-50'})
  )
  categoria_FK = forms.ModelChoiceField(
      label='Categoria',
      queryset=Categoria.objects.all(),
      widget=forms.Select(attrs={'class': 'form-select w-50'})
  )

  class Meta:
    model = Producto
    fields = [
        'nombre_producto',
        'precio_producto',
        'imagen',
        'stock',
        'marca_FK',
        'categoria_FK']

  def clean(self):
    cleaned_data = super().clean()
    nombre_producto = cleaned_data.get('nombre_producto')
    codigo_producto = cleaned_data.get('codigo_producto')

    # por si quiere agregar un mensaje adicional
    # if not nombre_producto:
    #     self.add_error('nombre_producto', 'El campo Nombre de Producto es requerido.')
    # elif not codigo_producto:
    #     self.add_error('codigo_producto', 'El campo Código de Producto es requerido.')
    if nombre_producto and codigo_producto:
      cleaned_data['nombre_producto'] = nombre_producto.upper()
      cleaned_data['codigo_producto'] = codigo_producto.upper()

    return cleaned_data


class ProductoAgregarForm(BaseProductoForm):
  codigo_producto = forms.CharField(
      label='Codigo del producto',
      widget=forms.TextInput(attrs={'class': 'form-control'})
  )

  class Meta:
    model = Producto
    fields = BaseProductoForm.Meta.fields + ['codigo_producto']


class ProductoEditarForm(BaseProductoForm):
  class Meta:
    model = Producto
    fields = BaseProductoForm.Meta.fields


# -----------------Añadido--Productos-------------


class PlusProductoForm(forms.ModelForm):

  precio_producto = forms.DecimalField(
      label='Precio del producto',
      widget=forms.NumberInput(attrs={'class': 'form-control'})
  )
  stock_increment = forms.DecimalField(
      label='Agregar al Stock',
      widget=forms.NumberInput(attrs={'class': 'form-control'}),
  )

  class Meta:
    model = Producto
    fields = ['precio_producto', 'stock_increment']

  def clean_stock_increment(self):
    stock_increment = self.cleaned_data.get('stock_increment')
    if stock_increment is not None and stock_increment < 1:
      raise forms.ValidationError(
          "El valor del stock incrementado debe ser al menos 1.")
    return stock_increment
