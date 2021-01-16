from .models import *
from rest_framework import serializers


class CustomUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['Name', 'Email', 'Outlook', 'Google_calendar']


class DistrictSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = District
        fields = ['Name', 'TimeFrame']


class CreditSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Credit
        fields = ['credit_type']

class CourseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Course
        fields = ['Name', 'Location', 'Price', 'Date','Provider','link']


