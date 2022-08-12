from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from requests import delete
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from mailing.serializers import *
from mailing.models import *
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import permissions
from mailing.permissions import IsOwnerOrReadOnly
from django.contrib.auth.models import User
from rest_framework import viewsets
from drf_yasg.utils import swagger_auto_schema
from .postman import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.settings import api_settings

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'mails': reverse('mail-list', request=request, format=format)
    })

# def index(request):
#     mail = Mail.objects.all()[0]
#     data = MailSerializer(mail)
#     content = JSONRenderer().render(data.data)

#     return HttpResponse(content)


# class MailList(generics.ListCreateAPIView):
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#     queryset = Mail.objects.all()
#     serializer_class = MailSerializer

#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)



# class MailDetail(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly,
#                       IsOwnerOrReadOnly]
#     queryset = Mail.objects.all()
#     serializer_class = MailSerializer

# class ClientList(generics.ListCreateAPIView):
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#     queryset = Client.objects.all()
#     serializer_class = ClientSerializer




# class ClientDetail(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#     queryset = Client.objects.all()
#     serializer_class = ClientSerializer

class MailViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Mail.objects.all()
    serializer_class = MailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]


    def perform_update(self, serializer):
        mail = serializer.save()
        editMailing(mail)
        
    def perform_create(self, serializer):
        mail = serializer.save(owner=self.request.user)
        addMailing(mail)
    


class ClientViewSet(viewsets.ModelViewSet):

    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    hello world
    """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]


    def perform_create(self, serializer):
        serializer.save()

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

class MailStats(APIView):
    @swagger_auto_schema(
        operation_description="Get detailed stats"
    )
    def get(self, request, format=None):
        data = {
            "total_mails":Mail.objects.all().count(),
            "total_messages":Message.objects.all().count(),
            "total_send":Message.objects.filter(status="S").count(),
            "total_failed":Message.objects.filter(status="F").count(),
        }
        serializer = MailStatSerializer(data)
        return Response(serializer.data)
    
class OneMailStats(APIView):

    @swagger_auto_schema(
        operation_description="Get detailed stats for one mail"
    )
    def get(self, request,pk, format=None):
        data = {
            "total_messages":Message.objects.filter(related_mail = pk).count(),
            "total_send":Message.objects.filter(status="S",related_mail = pk).count(),
            "total_failed":Message.objects.filter(status="F",related_mail = pk).count(),
        }
        serializer = OneMailStatSerializer(data)
        return Response(serializer.data)