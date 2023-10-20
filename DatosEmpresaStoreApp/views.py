from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import update_session_auth_hash
# Modelos y formularios
from .forms import DatosEmpresaEditarContactoForm, UsuarioEditarContactoForm, CambiarContrasenaForm
from .models import DatosEmpresa


# --------------------SETTING---------------------

@login_required(login_url='/login/')
def editar_registros(request):
  empresa = DatosEmpresa.objects.get(pk=1)
  usuario_autenticado = request.user

  form_uno = DatosEmpresaEditarContactoForm(instance=empresa)
  form_dos = UsuarioEditarContactoForm(instance=usuario_autenticado)
  form_cambio_clave = CambiarContrasenaForm(user=usuario_autenticado)

  if request.method == 'POST':
    if 'submit_form_uno' in request.POST:
      form_uno = DatosEmpresaEditarContactoForm(request.POST, instance=empresa)
      if form_uno.is_valid():
        form_uno.save()
        messages.success(request, "Datos del local actualizados Correctamente")
        return redirect('Setting')
    elif 'submit_form_dos' in request.POST:
      form_dos = UsuarioEditarContactoForm(
          request.POST, instance=usuario_autenticado)
      if form_dos.is_valid():
        form_dos.save()
        messages.success(
            request, "Datos de usuario actualizados Correctamente")
        return redirect('Setting')
    elif 'submit_form_pass' in request.POST:
      form_cambio_clave = CambiarContrasenaForm(
          user=usuario_autenticado,
          data=request.POST)
      if form_cambio_clave.is_valid():
        user = form_cambio_clave.save()
        update_session_auth_hash(request, user)
        messages.success(request, "Contraseña actualizada Correctamente")
        return redirect('Setting')

  return render(request, 'setting.html', {
      'form_uno': form_uno,
      'form_dos': form_dos,
      'empresa': empresa,
      'form_pass': form_cambio_clave
  })
