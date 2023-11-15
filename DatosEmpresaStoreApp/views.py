from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from utils.custom_middleware import cargo_check

# Modelos y formularios
from .forms import DatosEmpresaEditarContactoForm
from .models import DatosEmpresa

# Prodcutos formulario
from ProductosStoreApp.forms import CategoriaAgregarForm

# --------------------SETTING---------------------


@login_required(login_url="/login/")
@cargo_check
def editar_datos_empresa(request):
    empresa = get_object_or_404(DatosEmpresa, pk=1)
    form_empresa = DatosEmpresaEditarContactoForm(instance=empresa)
    form_categoria = CategoriaAgregarForm

    if request.method == "POST":
        if "submit_form_empresa" in request.POST:
            form_empresa = DatosEmpresaEditarContactoForm(
                request.POST, instance=empresa
            )
            if form_empresa.is_valid():
                form_empresa.save()
                messages.success(request, "Datos del local actualizados correctamente")
                return redirect("Setting")

        elif "submit_form_categoria" in request.POST:
            form_categoria = CategoriaAgregarForm(request.POST)

            if form_categoria.is_valid():
                form_categoria.save()
                messages.success(request, "Categoría añadida correctamente")
                return redirect("Setting")

    return render(
        request,
        "setting.html",
        {
            "form_empresa": form_empresa,
            "empresa": empresa,
            "form_categoria": form_categoria,
        },
    )
