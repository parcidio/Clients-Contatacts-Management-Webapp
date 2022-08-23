from django.urls import path
from . import views


urlpatterns = [
    path("", views.getRoutes, name="routes"),
    path("clients/", views.getClients, name="clients"),
    path("contacts/", views.getContacts, name="contacts"),

    path("clients/create/", views.createClient, name="create-client"),
    path("contacts/create/", views.createContact, name="create-contact"),
    path("clients/<str:pk>/update/", views.updateClient, name="update-client"),
    path("contacts/<str:pk>/update/", views.updateContact, name="update-contact"),
    path("clients/<str:pk>/delete/", views.deleteClient, name="delete-client"),
    path("contacts/<str:pk>/delete/", views.deleteContact, name="delete-contact"),

    path("contacts/<str:pk>/link/", views.LinkClientToContact, name="link-contact"),
    path("clients/<str:pk>/getlinks/",
         views.getRelatedContacts, name="contact-links"),

    path("clients/<str:pk>/", views.getClient, name="client"),
    path("contacts/<str:pk>/", views.getContact, name="contact"),



]
