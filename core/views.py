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
from django.http import JsonResponse
from django.core import serializers

# Create your views here.
def index(request):
    return HttpResponse("Hello, world.")

class Home(APIView):
    def get(self, request, pk):

        response_data = {}
        
        user = User.objects.filter(pk=pk)

        if not user.exists() :
            return Response(str(request.data), status=status.HTTP_404_NOT_FOUND) 


        ### USER DATA ###
        response_data['id'] = user[0].pk
        response_data['name'] = user[0].Name
        response_data['email'] = user[0].Email
        response_data['outlook'] = user[0].Outlook
        response_data['google_calendar'] = user[0].Google_calendar
        response_data['date_created'] = user[0].date_created.isoformat()

        ### USER_DISTRICT DATA ###
        userdistrict = User_District.objects.filter(user=user[0])
        ud_list = []
        if userdistrict.exists():
            district = {}
            for ud in userdistrict:
                district['name'] = ud.district.Name
                district['timeframe'] = ud.district.TimeFrame.total_seconds()

                districtcredits = District_Credit.objects.filter(district=ud.district)

                for dc in districtcredits:
                    district['credit_type'] = dc.credit.credit_type
                    district['credit_amount'] = dc.amount
                ud_list.append(district)

        ### USER_COURSES DATA ###
        usercourses = User_Course.objects.filter(user=user[0])
        uc_list = []

        if usercourses.exists():
            course = {}
            for uc in usercourses:
                course['id'] = uc.course.id
                course['status'] = uc.status

                coursecredits = Course_Credit.objects.filter(course=uc.course)
                course_credit = {}
                cc_list = []
                for cc in coursecredits:
                    course_credit['course_id'] = cc.course.id
                    course_credit['course_credit_id'] = cc.credit.id
                    course_credit['course_credit_amount'] = cc.amount
                    cc_list.append(course_credit)
                course['course_credit'] = cc_list

            uc_list.append(course)

        ### USER_FAVORITED ###

        userfavorited = User_Favorited.objects.filter(user=user[0])
        uf_list = []

        if userfavorited.exists():
            for uf in userfavorited:
                uf_list.append(uf.course.id)


        ### PUT TOGETHER ###
        if ud_list:
            response_data['districts'] = ud_list

        if uc_list:
            response_data['courses_enrolled'] = uc_list

        if uf_list:
            response_data['user_favorited'] = uf_list


        
        return Response(json.dumps(response_data))



class Enroll(APIView):
	parser_classes = [JSONParser]

	def post(self, request, format=None):
		user = User.objects.filter(pk=request.data.get('user'))
		course = Course.objects.filter(pk=request.data.get('course'))

		if not user.exists() or not course.exists():
			return Response(str(request.data), status=status.HTTP_404_NOT_FOUND) 

		if User_Course.objects.filter(user=user[0],course=course[0]).exists():
			return Response(str(request.data), status=status.HTTP_409_CONFLICT) 

		usercourse = User_Course(user=user[0], course=course[0], status='ST')
		usercourse.save()

		return Response(str(request.data), status=status.HTTP_201_CREATED)

class Favorited(APIView):
    parser_classes = [JSONParser]

    def post(self, request, format=None):
        user = User.objects.filter(pk=request.data.get('user'))
        course = Course.objects.filter(pk=request.data.get('course'))

        if not user.exists() or not course.exists():
            return Response(str(request.data), status=status.HTTP_404_NOT_FOUND) 

        if User_Favorited.objects.filter(user=user[0],course=course[0]).exists():
            return Response(str(request.data), status=status.HTTP_409_CONFLICT) 

        userfav = User_Favorited(user=user[0], course=course[0])
        userfav.save()

        return Response(str(request.data), status=status.HTTP_201_CREATED)


class addDistrictUser(APIView):
    parser_classes = [JSONParser]

    def post(self, request, format=None):
        user = User.objects.filter(pk=request.data.get('user'))
        districts = District.objects.filter(pk__in=request.data.get('districts'))

        if not user.exists() or not districts.exists():
            return Response(str(request.data), status=status.HTTP_404_NOT_FOUND) 

        for district in districts:
            if not User_District.objects.filter(user=user[0],district=district).exists():
                userDistrict = User_District(user=user[0], district=district)
                userDistrict.save()

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
