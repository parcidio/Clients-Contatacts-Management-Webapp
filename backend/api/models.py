from django.db import models

# All fields should be optional


class Client(models.Model):
    name = models.CharField(max_length=254, null=True, blank=True)
    client_code = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=254, null=True, blank=True)
    surname = models.CharField(max_length=254, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    linked_clients = models.ManyToManyField(
        Client, related_name="Links", null=True, blank=True)

    def __str__(self):
        return self.name + " " + self.surname
