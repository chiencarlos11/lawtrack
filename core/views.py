from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
from rest_framework.parsers import JSONParser

# Create your views here.
def index(request):
    return HttpResponse("Hello, world.")

class Enroll(APIView):
	parser_classes = [JSONParser]

	def post(self, request, format=None):


		user = User.objects.filter(pk=request.data.get('user'))
		course = Course.objects.filter(pk=request.data.get('course'))

		if not user.exists() or not course.exists():
			return Response(str(request.data), status=status.HTTP_404_NOT_FOUND) 

		if User_Course.objects.filter(user=user[0],course=course[0]).exists():
			return Response(str(request.data), status=status.HTTP_409_CONFLICT) 

		usercourse = User_Course(user=user[0], course=course[0], isAdded=False, status='ST')
		usercourse.save()

		return Response(str(request.data), status=status.HTTP_201_CREATED)

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
