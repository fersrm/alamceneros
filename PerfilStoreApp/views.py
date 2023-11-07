from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import update_session_auth_hash
# Modelos y formularios
from .forms import UsuarioEditarContactoForm, CambiarContrasenaForm


# --------------------SETTING---------------------

@login_required(login_url='/login/')
def editar_perfil(request):

    usuario_autenticado = request.user

    form_contacto = UsuarioEditarContactoForm(instance=usuario_autenticado)
    form_cambio_clave = CambiarContrasenaForm(user=usuario_autenticado)

    if request.method == 'POST':
        if 'submit_form_contacto' in request.POST:
            form_contacto = UsuarioEditarContactoForm(
                request.POST, instance=usuario_autenticado)
            if form_contacto.is_valid():
                form_contacto.save()
                messages.success(
                    request, "Datos de usuario actualizados Correctamente")
                return redirect('Perfil')
        elif 'submit_form_pass' in request.POST:
            form_cambio_clave = CambiarContrasenaForm(
                user=usuario_autenticado,
                data=request.POST)
            if form_cambio_clave.is_valid():
                user = form_cambio_clave.save()
                update_session_auth_hash(request, user)
                messages.success(
                    request, "Contraseña actualizada Correctamente")
                return redirect('Perfil')

    return render(request, 'perfil.html', {
        'form_contacto': form_contacto,
        'form_pass': form_cambio_clave
    })
