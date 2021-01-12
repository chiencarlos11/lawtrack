from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(User)
admin.site.register(District)
admin.site.register(Credit)
admin.site.register(District_Credit)
admin.site.register(Course)
admin.site.register(User_Course)
admin.site.register(Course_Credit)