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

class PricingSerializer(serializers.Serializer):

    Name = serializers.CharField()
    Label = serializers.CharField()
    Currency = serializers.CharField()
    Price = serializers.FloatField()

    class Meta:
        model = Pricing
        fields = ('Name','Label','Currency','Price')

class CourseCreditSerializer(serializers.Serializer):

    credit = CreditSerializer()
    district = DistrictSerializer()
    amount = serializers.FloatField()

    class Meta:
        model = Course_Credit
        fields = ('credit','district','amount')

class CourseSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    Name = serializers.CharField()
    Location = serializers.CharField()
    Date = serializers.DateTimeField()
    Provider = serializers.CharField()
    link = serializers.URLField()
    logo = serializers.URLField()
    isArchived = serializers.BooleanField()
    pricing = PricingSerializer(many=True, read_only=True)
    courseCredit = CourseCreditSerializer(many=True, read_only=True)

    



