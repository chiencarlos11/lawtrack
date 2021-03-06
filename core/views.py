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
from rest_framework import pagination
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404

# Create your views here.
def index(request):
    return HttpResponse("Hello, world.")

# class Home(APIView):
#     def get(self, request, pk):

#         response_data = {}
        
#         user = User.objects.filter(pk=pk)

#         if not user.exists() :
#             return Response(str(request.data), status=status.HTTP_404_NOT_FOUND) 


#         ### USER DATA ###
#         response_data['id'] = user[0].pk
#         response_data['name'] = user[0].Name
#         response_data['email'] = user[0].Email
#         response_data['outlook'] = user[0].Outlook
#         response_data['google_calendar'] = user[0].Google_calendar
#         response_data['date_created'] = user[0].date_created.isoformat()

#         ### USER_DISTRICT DATA ###
#         userdistrict = User_District.objects.filter(user=user[0])
#         ud_list = []
#         if userdistrict.exists():
#             district = {}
#             for ud in userdistrict:
#                 district['name'] = ud.district.Name
#                 district['timeframe'] = ud.district.TimeFrame.total_seconds()

#                 districtcredits = District_Credit.objects.filter(district=ud.district)

#                 for dc in districtcredits:
#                     district['credit_type'] = dc.credit.credit_type
#                     district['credit_amount'] = dc.amount
#                 ud_list.append(district)

#         ### USER_COURSES DATA ###
#         usercourses = User_Course.objects.filter(user=user[0])
#         uc_list = []

#         if usercourses.exists():
#             course = {}
#             for uc in usercourses:
#                 course['id'] = uc.course.id
#                 course['status'] = uc.status

#                 coursecredits = Course_Credit.objects.filter(course=uc.course)
#                 course_credit = {}
#                 cc_list = []
#                 for cc in coursecredits:
#                     course_credit['course_id'] = cc.course.id
#                     course_credit['course_credit_id'] = cc.credit.id
#                     course_credit['course_credit_amount'] = cc.amount
#                     cc_list.append(course_credit)
#                 course['course_credit'] = cc_list

#             uc_list.append(course)

#         ### USER_FAVORITED ###

#         userfavorited = User_Favorited.objects.filter(user=user[0])
#         uf_list = []

#         if userfavorited.exists():
#             for uf in userfavorited:
#                 uf_list.append(uf.course.id)


#         ### PUT TOGETHER ###
#         if ud_list:
#             response_data['districts'] = ud_list

#         if uc_list:
#             response_data['courses_enrolled'] = uc_list

#         if uf_list:
#             response_data['user_favorited'] = uf_list


        
#         return Response(json.dumps(response_data))


# class CourseViewSet(APIView, pagination.LimitOffsetPagination):
#     def get(self, request):
#         response_data = []
#         courses = []
#         prices = []

#         #return all courses
#         courses = Course.objects.all()

#         for course in courses:
#             prices = Pricing.objects.filter(course=course)

#             course_data = {"Name": course.Name,
#                                 "Location": course.Location,
#                                 "Date": course.Date.isoformat(),
#                                 "Provider": course.Provider,
#                                 "link": course.link,
#                                 "logo": course.logo,
#                                 "isArchived": course.isArchived}
#             price_data = []
#             for price in prices:
#                 p = {"Name":price.Name,
#                         "Label":price.Label,
#                         "Currency":price.Currency,
#                         "Price":price.Price}
#                 price_data.append(p)
#             course_data['Pricing'] = price_data

#             #Course_Credit

#             course_credits = Course_Credit.objects.filter(course=course)

#             cc_data = []
#             for cc in course_credits:
#                 c = {
#                     "Credit": cc.credit.credit_type,
#                     "district": cc.district.Name,
#                     "district duration": cc.district.TimeFrame,
#                     "amount": cc.amount
#                 }
#                 cc_data.append(c)
#             course_data['Course Credit'] = price_data
#             response_data.append(course_data)

#         results = self.paginate_queryset(response_data, request, view=self)
#         serialized = json.dumps(results)
#         return self.get_paginated_response(serialized)



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

    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PageNumberPagination
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]

    # def list(self, request):
    #     queryset = Course.objects.all()
    #     serializer = CourseSerializer(queryset, many=True)
    #     return Response(serializer.data)

    # def retrieve(self, request, pk=None):
    #     queryset = Course.objects.all()
    #     course = get_object_or_404(queryset, pk=pk)
    #     serializer = CourseSerializer(course)
    #     return Response(serializer.data)
    

class PricingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Pricing.objects.all()
    serializer_class = PricingSerializer
    permission_classes = [permissions.IsAuthenticated]

class CourseCreditViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Course_Credit.objects.all()

    serializer_class = CourseCreditSerializer
    permission_classes = [permissions.IsAuthenticated]


