from django.contrib import admin
from django_tenants.admin import TenantAdminMixin
from django_tenants.utils import get_public_schema_name

from ClientSharedApp.models import Client, Domain


class PublicTenantAdminMixin(TenantAdminMixin):
    def has_module_permission(self, request):
        return request.tenant.schema_name == get_public_schema_name()


@admin.register(Client)
class ClientAdmin(PublicTenantAdminMixin, admin.ModelAdmin):
    list_display = ("name", "paid_until")


@admin.register(Domain)
class DomainAdmin(PublicTenantAdminMixin, admin.ModelAdmin):
    pass
