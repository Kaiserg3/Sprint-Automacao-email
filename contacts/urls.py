from django.urls import path
from . import views

urlpatterns = [
    path("contatos/", views.contato_list, name="contato_list"),
    path("contatos/novo/", views.contato_create, name="contato_create"),
    path("contatos/<int:pk>/editar/", views.contato_update, name="contato_update"),
    path("contatos/<int:pk>/excluir/", views.contato_delete, name="contato_delete"),

    path("envios/", views.envio_list, name="envio_list"),
    path("envios/novo/", views.envio_create, name="envio_create"),
    path("envios/<int:pk>/editar/", views.envio_update, name="envio_update"),
    path("envios/<int:pk>/excluir/", views.envio_delete, name="envio_delete"),
]
