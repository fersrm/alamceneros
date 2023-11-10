from django.urls import path
from django.contrib.auth.views import LoginView
from SistemaStoreApp import views

urlpatterns = [
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("", views.HomeView.as_view(), name="Home"),
    path("salir/", views.SalirView.as_view(), name="salir"),
]
