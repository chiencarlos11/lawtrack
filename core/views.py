from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import *

# Create your views here.
def index(request):
    return HttpResponse("Hello, world.")


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_created')
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]


class DistrictViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = District.objects.all().order_by('-Name')
    serializer_class = DistrictSerializer
    permission_classes = [permissions.IsAuthenticated]

class CreditViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Credit.objects.all().order_by('-credit_type')
    serializer_class = CreditSerializer
    permission_classes = [permissions.IsAuthenticated]

class CourseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Course.objects.all().order_by('-Name')
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]
