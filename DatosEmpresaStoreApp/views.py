from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render

# Modelos y formularios
from .forms import DatosEmpresaEditarContactoForm
from .models import DatosEmpresa

# Prodcutos formulario
from ProductosStoreApp.forms import CategoriaAgregarForm

# --------------------SETTING---------------------


@login_required(login_url='/login/')
def editar_datos_empresa(request):
    empresa = DatosEmpresa.objects.get(pk=1)
    form_empresa = DatosEmpresaEditarContactoForm(instance=empresa)
    form_categoria = CategoriaAgregarForm

    if request.method == 'POST':
        if 'submit_form_empresa' in request.POST:
            form_empresa = DatosEmpresaEditarContactoForm(
                request.POST, instance=empresa)
            if form_empresa.is_valid():
                form_empresa.save()
                messages.success(
                    request, "Datos del local actualizados Correctamente")
                return redirect('Setting')

        elif 'submit_form_categoria' in request.POST:
            form_categoria = CategoriaAgregarForm(request.POST)

            if form_categoria.is_valid():
                form_categoria.save()
                messages.success(
                    request, "Categoria Añadida Corestamente")
                return redirect('Setting')

    return render(request, 'setting.html', {
        'form_empresa': form_empresa,
        'empresa': empresa,
        'form_categoria': form_categoria
    })
