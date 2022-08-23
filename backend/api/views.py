from urllib import response
from xmlrpc import client
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from .serializers import *
import re
import string
from itertools import product

from rest_framework import routers, serializers, viewsets, status
from rest_framework.response import Response
from django.contrib.auth.models import User


from rest_framework import filters


# ===================


@api_view(['GET'])
def getRoutes(request):
    routes = [
        {
            'Endpoint': '/clients/',
            'method': 'GET',
            'body': None,
            'description': 'Returns an array of clients'
        },
        {
            'Endpoint': '/clients/id',
            'method': 'GET',
            'body': None,
            'description': 'Returns a single client object'
        },
        {
            'Endpoint': '/clients/create/',
            'method': 'POST',
            'body': {'body': ""},
            'description': 'Creates new client with data sent in post request'
        },
        {
            'Endpoint': '/clients/id/update/',
            'method': 'PUT',
            'body': {'body': ""},
            'description': 'Updates an existing client with data sent in post request'
        },
        {
            'Endpoint': '/clients/id/delete/',
            'method': 'DELETE',
            'body': None,
            'description': 'Deletes and exiting client'
        },
        {
            'Endpoint': '/contacts/',
            'method': 'GET',
            'body': None,
            'description': 'Returns an array of contacts'
        },
        {
            'Endpoint': '/contacts/id',
            'method': 'GET',
            'body': None,
            'description': 'Returns a single contact object'
        },
        {
            'Endpoint': '/contacts/create/',
            'method': 'POST',
            'body': {'body': ""},
            'description': 'Creates new contact with data sent in post request'
        },
        {
            'Endpoint': '/contacts/id/update/',
            'method': 'PUT',
            'body': {'body': ""},
            'description': 'Updates an existing contact with data sent in post request'
        },
        {
            'Endpoint': '/contacts/id/delete/',
            'method': 'DELETE',
            'body': None,
            'description': 'Deletes and exiting contact'
        },
    ]
    return Response(routes)

# CLIENTS VIEWS


@api_view(['GET'])
def getClients(request):
    clients = Client.objects.all()
    serializer = ClientSerializer(clients, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getClient(request, pk):
    client = Client.objects.get(id=pk)
    serializer = ClientSerializer(client, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def createClient(request):
    data = request.data
    clientCode = generateClientCode(str(data['name']))
    client = Client.objects.create(
        name=data['name'],
        client_code=clientCode
    )
    serializer = ClientSerializer(client, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
def updateClient(request, pk):
    data = request.data
    client = Client.objects.get(id=pk)
    serializer = ClientSerializer(instance=client, data=data)

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['DELETE'])
def deleteClient(request, pk):
    client = Client.objects.get(id=pk)
    client.delete()
    return Response("Note was deleted")


# CONTACT VIEWS
@ api_view(['GET'])
def getContacts(request):
    contacts = Contact.objects.all()
    serializer = ContactSerializer(contacts, many=True)
    return Response(serializer.data)


@ api_view(['GET'])
def getContact(request, pk):
    contact = Contact.objects.get(id=pk)
    serializer = ContactSerializer(contact, many=False)
    return Response(serializer.data)


@ api_view(['POST'])
def createContact(request):
    data = request.data
    contact = Contact.objects.create(
        name=data['name'], surname=data['surname'], email=data['email']
    )
    serializer = ContactSerializer(contact, many=False)
    return Response(serializer.data)


@ api_view(['PUT'])
def updateContact(request, pk):
    data = request.data

    contact = Contact.objects.get(id=pk)
    serializer = ContactSerializer(instance=contact, data=data)
    print(serializer)

    # # if serializer.is_valid():
    # serializer.add()
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@ api_view(['DELETE'])
def deleteContact(request, pk):
    contact = Contact.objects.get(id=pk)
    contact.delete()
    return Response("Note was deleted")


# Other helping functions
def generateClientCode(clientName):
    trimedClientName = clientName.strip()
    cleanClientName = re.sub(r'[^A-Za-z]', ' ', trimedClientName)
    clientNameSequence = cleanClientName.split()
    mergedclientName = "".join(clientNameSequence)
    alphabet = string.ascii_lowercase
    accronym = ""
    print(cleanClientName)
    if (' ' in cleanClientName):
        if (len(clientNameSequence) >= 3):
            print("more than 3 letter")
            print(clientNameSequence)

            for word in clientNameSequence:
                accronym += word[0]
            accronym = accronym[:3].upper()
            return generateAlphanumeric(accronym)

        if (len(clientNameSequence) == 2 and len(mergedclientName) >= 3):
            print("less than 3 letter")
            print(clientNameSequence)
            accronym = ""
            for word in clientNameSequence:
                accronym += word[0]
                print("accr: "+accronym)
            for letter in accronym:
                mergedclientName = mergedclientName.replace(letter, "", 1)
            excludeAccronym = mergedclientName
            print(excludeAccronym)
            if (excludeAccronym != ""):
                if (excludeAccronym[:1] in clientNameSequence[0]):
                    accronym = accronym[:1] + \
                        excludeAccronym[:1] + accronym[1:]
                else:
                    accronym = accronym + excludeAccronym[:1]

            accronym = accronym.upper()
            return generateAlphanumeric(accronym)
        elif (len(clientNameSequence) == 1 and len(mergedclientName) >= 3):
            # take the 1st 3 letters
            accronym = mergedclientName[:3].upper()
            return generateAlphanumeric(accronym)

        elif (len(clientNameSequence) == 2 and len(mergedclientName) == 2):
            print("two letter")
            accronym = mergedclientName
            for letter in alphabet:
                accronym += letter
                accronym = accronym.upper()
                if (generateAlphanumeric(accronym)):
                    break
        return generateAlphanumeric(accronym)

    else:
        if (len(mergedclientName) >= 3):
            # take the 1st 3 letters
            accronym = mergedclientName[:3].upper()
            return generateAlphanumeric(accronym)
        if (len(mergedclientName) == 2):
            accronym = mergedclientName
            for letter in alphabet:
                accronym += letter
                accronym = accronym.upper()
                if (generateAlphanumeric(accronym)):
                    break
            return generateAlphanumeric(accronym)
        if (len(mergedclientName) == 1):
            accronym = mergedclientName
            # this will generate all possible 2 letter combinations of the letter in the alphabet
            alphabetPermutation = [''.join(i)
                                   for i in product(alphabet, repeat=2)]
            # print(alphabetPermutation)
            for letter in alphabetPermutation:
                accronym += letter
                accronym = accronym.upper()
                if (generateAlphanumeric(accronym)):
                    break
            return generateAlphanumeric(accronym)


def generateAlphanumeric(accronym):
    for numeric in range(1, 1000):
        numeric = f"{numeric:03}"
        alphaNumeric = accronym+numeric
        try:
            Client.objects.get(client_code=alphaNumeric)
            clientCodeExist = False
        except:
            clientCodeExist = alphaNumeric
            print(alphaNumeric)
            break

    return clientCodeExist


# LINKING CONTACTS TO CLIENTS
@ api_view(['PATCH', 'PUT'])
def LinkClientToContact(request, pk):
    contact = Contact.objects.get(id=pk)
    data = request.data.get("linked_clients")
    print("=====================LINK CLIENT=============================")
    print(data)
    contact.linked_clients.set(data)
    contact.save()
    serializer = ContactSerializer(contact)
    print(serializer)
    return Response(serializer.data)


@ api_view(['PATCH', 'PUT'])
def UnlinkClientToContact(request, pk):
    contact = Contact.objects.get(id=pk)
    data = request.data.get("linked_clients")
    print("========================UNLINK CLIENT==========================")
    print(data)
    contact.linked_clients.set(data)
    contact.save()
    serializer = ContactSerializer(contact)
    print(serializer)
    return Response(serializer.data)


@ api_view(['GET'])
def getRelatedContacts(request, pk):
    contacts = Contact.objects.filter(linked_clients__id=pk)

    serializer = ContactSerializer(contacts, many=True)
    return Response(serializer.data)
