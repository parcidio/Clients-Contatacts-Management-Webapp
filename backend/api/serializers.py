from dataclasses import field
from rest_framework.serializers import ModelSerializer

from .models import Client, Contact


class ClientSerializer(ModelSerializer):

    class Meta:
        model = Client
        fields = "__all__"
        depth = 1
        extra_kwargs = {'linked_contacts': {'required': False}}


class ContactSerializer(ModelSerializer):

    class Meta:
        model = Contact
        fields = "__all__"
        depth = 1
        extra_kwargs = {'linked_clients': {'required': False}}
