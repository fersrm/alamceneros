from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Usuario, Cargo

# --------------------Tabla Usuario ----------


class BaseUsuarioForm(forms.ModelForm):
    first_name = forms.CharField(
        label="Nombre", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    last_name = forms.CharField(
        label="Apellido", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    username = forms.CharField(
        label="Nombre de Usuario",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    telefono_user = forms.CharField(
        label="Teléfono", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    email = forms.EmailField(
        label="Email", widget=forms.EmailInput(attrs={"class": "form-control"})
    )
    cargo_FK = forms.ModelChoiceField(
        label="Cargo",
        queryset=Cargo.objects.exclude(pk=1),
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Usuario
        fields = [
            "first_name",
            "last_name",
            "username",
            "telefono_user",
            "email",
            "cargo_FK",
        ]

    def clean(self):
        cleaned_data = super().clean()
        nombre_usuario = cleaned_data.get("username")

        if nombre_usuario:
            cleaned_data["username"] = nombre_usuario.upper()

        cargo_fk = cleaned_data.get("cargo_FK")

        # Verifica si el cargo seleccionado tiene pk = 1 Administrador
        if cargo_fk and cargo_fk.pk == 1:
            raise forms.ValidationError("El cargo seleccionado no es válido")

        return cleaned_data


class UsuarioEditarForm(BaseUsuarioForm):
    class Meta(BaseUsuarioForm.Meta):
        fields = BaseUsuarioForm.Meta.fields


class UsuarioAgregarForm(UserCreationForm, BaseUsuarioForm):
    password1 = forms.CharField(
        label="Nueva Contraseña",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    password2 = forms.CharField(
        label="Confirmar Nueva Contraseña",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    class Meta(BaseUsuarioForm.Meta):
        fields = BaseUsuarioForm.Meta.fields + ["password1", "password2"]
