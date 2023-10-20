from django.contrib import admin
from UsuariosStoreApp.models import Usuario, Cargo
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.admin import UserAdmin

# Register your models here.

admin.site.register(Cargo)

# -----------------USUARIO----------------------------------------------

# para el formulario de creacion de usuarios


class CustomUserCreationForm(UserCreationForm):
  password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
  password2 = forms.CharField(
      label='Confirmar contraseña',
      widget=forms.PasswordInput)

  class Meta:
    model = Usuario
    fields = (
        'username',
        'first_name',
        'last_name',
        'email',
        'telefono_user',
        'password1',
        'password2',
        'cargo_FK')

  def clean_password2(self):
    password1 = self.cleaned_data.get('password1')
    password2 = self.cleaned_data.get('password2')
    if password1 and password2 and password1 != password2:
      raise forms.ValidationError('Las contraseñas no coinciden.')
    return password2

# esto es el formulario para editar el usuario


class CustomUserAdmin(UserAdmin):
  add_form = CustomUserCreationForm  # Utiliza el nuevo formulario personalizado
  add_fieldsets = (
      (None, {
          'classes': ('wide',),
          'fields': ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'cargo_FK'),
      }),
  )
  fieldsets = (
      (None, {'fields': ('first_name', 'last_name',
       'email', 'telefono_user', 'cargo_FK')}),
      ('Informacion', {'fields': ('username', 'password',)}),
      ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser',)}),
      # ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
      ('Advanced options', {
          'classes': ('collapse', 'wide', 'extrapretty'),
          'fields': ('groups', 'user_permissions',)}),
  )
  # lo que se muestra al listar usuarios
  list_display = (
      'username',
      'first_name',
      'last_name',
      'email',
      'cargo_FK',
      'is_staff')


admin.site.register(Usuario, CustomUserAdmin)
