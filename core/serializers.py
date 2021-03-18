from .models import *
from rest_framework import serializers


class CustomUserSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.CharField()

    class Meta:
        model = User
        fields = ['id','Name', 'Email', 'Outlook', 'Google_calendar']


class DistrictSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.CharField()

    class Meta:
        model = District
        fields = ['id','Name', 'TimeFrame']


class CreditSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.CharField()

    class Meta:
        model = Credit
        fields = ['id','credit_type']

class CourseSerializer(serializers.HyperlinkedModelSerializer):

    id = serializers.CharField()
    PriceModel = serializers.RelatedField(source='Pricing', read_only=True)

    class Meta:
        model = Course
        fields = ['id','Name', 'Location', 'Date','Provider','link','logo','isArchived']


