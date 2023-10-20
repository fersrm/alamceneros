# Librerías de Django
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.shortcuts import redirect
# Modelos y formularios
from .forms import UsuarioAgregarForm, UsuarioEditarForm
from .models import Usuario

# Para trabajar con clases

from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy

# imporat funciones
from utils.helpers import buscar_campos
# Create your views here.

# ---------------CRUD USUARIOS------------


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class UsuarioListView(ListView):
  model = Usuario
  template_name = 'usuarios.html'
  paginate_by = 7

  def get_queryset(self):
    busqueda = self.request.GET.get('buscar')
    campos_busqueda = [
        'first_name',
        'last_name',
        'username',
        'telefono_user',
        'email',
        'rol_FK__rol_usuario']
    queryset = buscar_campos(
        self.model, campos_busqueda, busqueda)
    queryset = queryset.order_by('-id')
    return queryset

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    paginator = Paginator(context['object_list'], self.paginate_by)
    page = self.request.GET.get('page')
    context['object_list'] = paginator.get_page(page)
    return context

# -------------------------------------------------


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class AgregarUsuarioView(CreateView):
  model = Usuario
  form_class = UsuarioAgregarForm
  template_name = 'modal/AddUser.html'

  def form_valid(self, form):
    form.save()
    messages.success(self.request, "Usuario agregado correctamente")
    return super().form_valid(form)

  def form_invalid(self, form):
    messages.error(self.request, 'Error en el formulario')
    for field, errors in form.errors.items():
      for error in errors:
        messages.error(self.request, f"{field}: {error}")
    return HttpResponseRedirect('/usuarios/')

  def get_success_url(self):
    return reverse_lazy('Usuarios')
# -------------------------------------------------


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class EditarUsuarioView(UpdateView):
  model = Usuario
  form_class = UsuarioEditarForm
  template_name = 'modal/EditUser.html'

  def form_valid(self, form):
    if self.object.is_superuser:  # Comprueba si el (superuser)
      messages.error(self.request, "No puedes editar al usuario ADMIN.")
      return HttpResponseRedirect('/usuarios/')

    form.clean()
    form.save()
    messages.success(self.request, "Usuario Editado correctamente")
    return super().form_valid(form)

  def form_invalid(self, form):
    messages.error(self.request, 'Error en el formulario')
    for field, errors in form.errors.items():
      for error in errors:
        messages.error(self.request, f"{field}: {error}")
    return HttpResponseRedirect('/usuarios/')

  def get_success_url(self):
    return reverse_lazy('Usuarios')
# --------------------------------------------------


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class EliminarUsuarioView(DeleteView):
  model = Usuario
  success_url = reverse_lazy('Usuarios')

  def get(self, request, *args, **kwargs):
    self.object = self.get_object()
    if self.object.is_superuser:  # Comprueba si el (superuser)
      messages.error(self.request, "No puedes eliminar al usuario ADMIN.")
      return redirect(self.get_success_url())

    messages.success(self.request, "Usuario eliminado correctamente")
    self.object.delete()
    return redirect(self.get_success_url())

#
