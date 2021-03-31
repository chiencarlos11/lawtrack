import csv
import json
import datetime
from core.models import *
from django.conf import settings
from django.utils.timezone import make_aware


def run():
    with open('Initial_Data_for_script.tsv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        currency = "CA"

        substantiveCredits = Credit.objects.get(credit_type='Substantive Credits')
        ontario = District.objects.get(Name='Ontario')

        for row in csv_reader:
            print(f'\t{row[0]}\t{row[1]}\t{row[2]}')
            if row[0] == "Taking the Lead: Winning Strategies & Tips For Commercial Cases":
                currency = "US"

            course = None
            if not Course.objects.filter(Name=row[0]).exists():
                course = Course(Name=row[0], 
                                    Location=row[1], 
                                    Date=make_aware(datetime.datetime.today()), 
                                    Provider=row[2], 
                                    link=row[3], 
                                    logo="")
                course.save()

                
            else:
                course = Course.objects.filter(Name=row[0]).first()
                course.Name=row[0]
                course.Location=row[1]
                course.Date=make_aware(datetime.datetime.today())
                course.Provider=row[2]
                course.link=row[3]
                course.logo=""     
                course.save()

            price = 0
            priceDict = {}
            try:
                if price == "":
                    price = 0
                else:
                    price = int(row[4])
            except ValueError:
                print(row[4])
                priceDict = json.loads(row[4])

            if not Pricing.objects.filter(Name=row[0]).exists():
                if priceDict:
                    for key in priceDict:
                        newPrice = Pricing(Name=row[0],Label=key,Currency=currency,Price=priceDict[key], course=course)
                        newPrice.save()
                else:
                    newPrice = Pricing(Name=row[0],Label='Standard',Currency=currency,Price=price, course=course)
                    newPrice.save()

            print("credit = " + str(substantiveCredits))
            print("district = " + str(ontario))
            print("course = " + str(course))
            print("amount = " + str(row[5]))
            if not Course_Credit.objects.filter(credit=substantiveCredits, course=course, district=ontario).exists():
                print("inserting now")
                newCourseCredit = Course_Credit(credit=substantiveCredits, course=course, district=ontario, amount=int(row[5]))
                newCourseCredit.save()