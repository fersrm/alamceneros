from django import forms
from .models import Producto, Categoria
from .choices import tipoMedida, tipoImpuesto
# -------------------------Productos--------------


class BaseProductoForm(forms.ModelForm):

    precio_bruto_producto = forms.DecimalField(
        label='Precio Bruto',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    margen_ganancia = forms.DecimalField(
        label='Margen de Ganancia %',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'readonly': 'readonly'}),
        required=False
    )

    precio_venta = forms.DecimalField(
        label='Precio de Venta',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Producto
        fields = [
            'precio_bruto_producto',
            'margen_ganancia',
            'precio_venta']

    def clean(self):
        cleaned_data = super().clean()
        descripcion_producto = cleaned_data.get('descripcion_producto')

        if descripcion_producto:
            cleaned_data['descripcion_producto'] = descripcion_producto.upper()

        return cleaned_data


class ProductoEditarForm(BaseProductoForm):

    descripcion_producto = forms.CharField(
        label='Descripcion',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    imagen = forms.ImageField(
        label='Imagen',
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        required=False
    )

    stock = forms.DecimalField(
        label='Stock',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    tipo_medida = forms.ChoiceField(
        label='Medida',
        choices=tipoMedida,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    tipo_impuesto = forms.ChoiceField(
        label='Impuesto',
        choices=tipoImpuesto,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    categoria_FK = forms.ModelChoiceField(
        label='Categoria',
        queryset=Categoria.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Producto
        fields = BaseProductoForm.Meta.fields + [
            'descripcion_producto',
            'imagen',
            'stock',
            'tipo_impuesto',
            'tipo_medida',
            'categoria_FK']


class ProductoAgregarForm(ProductoEditarForm):
    codigo_producto = forms.CharField(
        label='Codigo',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'autofocus': True})
    )

    class Meta:
        model = Producto
        fields = ProductoEditarForm.Meta.fields + ['codigo_producto']

    def clean(self):
        cleaned_data = super().clean()
        descripcion_producto = cleaned_data.get('descripcion_producto')
        codigo_producto = cleaned_data.get('codigo_producto')

        if descripcion_producto and codigo_producto:
            cleaned_data['descripcion_producto'] = descripcion_producto.upper()
            cleaned_data['codigo_producto'] = codigo_producto.upper()

        return cleaned_data

# -----------------Añadido--Productos-------------


class PlusProductoForm(BaseProductoForm):

    precio_bruto_old = forms.DecimalField(
        label='Precio bruto antiguo',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'readonly': 'readonly'})
    )

    stock_increment = forms.DecimalField(
        label='Agregar al Stock',
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Producto
        fields = BaseProductoForm.Meta.fields + [
            'precio_bruto_old', 'stock_increment'
        ]

    def __init__(self, *args, **kwargs):
        super(PlusProductoForm, self).__init__(*args, **kwargs)
        self.fields['precio_bruto_old'].initial = self.instance.precio_bruto_producto

    def clean_stock_increment(self):
        stock_increment = self.cleaned_data.get('stock_increment')
        if stock_increment is not None and stock_increment < 1:
            raise forms.ValidationError(
                "El valor del stock incrementado debe ser al menos 1.")
        return stock_increment


# ----------------Agregar categoria--------------

class CategoriaAgregarForm(forms.ModelForm):

    nombre_categoria = forms.CharField(
        label='Nueva Categoria',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Categoria
        fields = ['nombre_categoria',]

    def clean(self):
        cleaned_data = super().clean()
        nombre_categoria = cleaned_data.get('nombre_categoria')

        if nombre_categoria:
            cleaned_data['nombre_categoria'] = nombre_categoria.upper()

        return cleaned_data
