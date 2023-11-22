from django.dispatch import receiver
from django.db.models.signals import post_migrate
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Cargo(models.Model):
    id_cargo = models.AutoField(primary_key=True)
    cargo_usuario = models.CharField(max_length=45, unique=True)

    def save(self, *args, **kwargs):
        if self.pk is None:
            last_instance = Cargo.objects.order_by("-id_cargo").first()

            if last_instance.id_cargo:
                self.id_cargo = last_instance.id_cargo + 1

        super(Cargo, self).save(*args, **kwargs)

    class Meta:
        db_table = "cargo"

    def __str__(self):
        return f"{self.cargo_usuario}"


class Usuario(AbstractUser):
    telefono_user = models.CharField(max_length=15, default="123456789")
    cargo_FK = models.ForeignKey(
        Cargo, on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        db_table = "usuario"


@receiver(post_migrate)
def create_default_roles(sender, **kwargs):
    if sender.name == "UsuariosStoreApp":
        Cargo.objects.get_or_create(
            id_cargo=1, defaults={"cargo_usuario": "Administrador"}
        )
        Cargo.objects.get_or_create(
            id_cargo=2, defaults={"cargo_usuario": "Jefe de Ventas"}
        )
        Cargo.objects.get_or_create(id_cargo=3, defaults={"cargo_usuario": "Vendedor"})
