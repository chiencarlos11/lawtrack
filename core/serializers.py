from .models import *
from rest_framework import serializers


class CustomUserSerializer(serializers.Serializer):

    id = serializers.CharField()

    class Meta:
        model = User
        fields = ['id','Name', 'Email', 'Outlook', 'Google_calendar']


class DistrictSerializer(serializers.Serializer):

    Name = serializers.CharField()
    TimeFrame = serializers.DurationField()

    class Meta:
        model = District
        fields = ['id','Name', 'TimeFrame']


class CreditSerializer(serializers.Serializer):

    credit_type = serializers.CharField()

    class Meta:
        model = Credit
        fields = ['id','credit_type']

class CourseSerializer(serializers.Serializer):

    Name = serializers.CharField()
    Location = serializers.CharField()
    Date = serializers.DateTimeField()
    Provider = serializers.CharField()
    link = serializers.URLField()
    logo = serializers.URLField()
    isArchived = serializers.BooleanField()

class PricingSerializer(serializers.Serializer):

    Name = serializers.CharField()
    Label = serializers.CharField()
    Currency = serializers.CharField()
    Price = serializers.FloatField()
    Currency = serializers.CharField()
    course = CourseSerializer()


class CourseCreditSerializer(serializers.Serializer):

    credit = CreditSerializer()
    course = CourseSerializer()
    district = DistrictSerializer()
    amount = serializers.FloatField()
    



