from .models import *
from rest_framework import serializers


class CustomUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id','Name', 'Email', 'Outlook', 'Google_calendar']


class DistrictSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = District
        fields = ['id','Name', 'TimeFrame']


class CreditSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Credit
        fields = ['id','credit_type']

class CourseSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.CharField()

    class Meta:
        model = Course
        fields = ['id','Name', 'Location', 'Price', 'Date','Provider','link']


