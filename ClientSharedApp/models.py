from django.db import models
from django_tenants.models import TenantMixin, DomainMixin
from django_tenants.utils import get_tenant_type_choices


class Client(TenantMixin):
  name = models.CharField(max_length=100)
  paid_until = models.DateField()
  on_trial = models.BooleanField()
  created_on = models.DateField(auto_now_add=True)
  type = models.CharField(max_length=100, choices=get_tenant_type_choices())
  # default true, schema will be automatically created and synced when it is
  # saved
  auto_create_schema = True


class Domain(DomainMixin):
  pass
