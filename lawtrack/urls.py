"""lawtrack URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from core.views import UserViewSet, DistrictViewSet, CreditViewSet, CourseViewSet, Enroll, PricingViewSet, CourseCreditViewSet


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'districts', DistrictViewSet)
router.register(r'credits', CreditViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'pricing', PricingViewSet)
router.register(r'course_credit', CourseCreditViewSet)

urlpatterns = [
    path('core/', include('core.urls')),
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    # path('enroll/', Enroll.as_view()),
    # path('courses/', CourseViewSet.as_view())
]

