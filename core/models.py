from django.db import models

# Create your models here.
class User(models.Model):
	Name = models.CharField(max_length=200)
	Email = models.EmailField()
	Outlook = models.CharField(max_length=200)
	Google_calendar = models.CharField(max_length=200)
	date_created = models.DateTimeField(auto_now_add=True, blank=True)
	
	def __str__(self):
		return self.Name

class District(models.Model):
	Name = models.CharField(max_length=200)
	TimeFrame = models.DurationField()
	def __str__(self):
		return self.Name

class User_District(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	district = models.ForeignKey(District, on_delete=models.CASCADE)
	def __str__(self):
		return str(self.user) + " - " + str(self.district)

class Credit(models.Model):
	credit_type = models.CharField(max_length=200)

	def __str__(self):
		return self.credit_type

class District_Credit(models.Model):
	district = models.ForeignKey(District, on_delete=models.CASCADE)
	credit = models.ForeignKey(Credit, on_delete=models.CASCADE)
	amount = models.DecimalField(max_digits=5, decimal_places=2)

	def __str__(self):
		return str(self.district) + " - " + str(self.credit) + " - " + str(self.amount)

class Course(models.Model):

	Name = models.CharField(max_length=200)
	Location = models.CharField(max_length=200)
	Date = models.DateTimeField(blank=True)
	Provider = models.CharField(max_length=200)
	link = models.URLField(default=None,blank=True)
	logo = models.URLField(default=None,blank=True, null=True)
	isArchived = models.BooleanField(default=False,blank=True, null=True)

	def __str__(self):
		return self.Name

class Pricing(models.Model):
	CURRENCY = [
		('US', 'USD'),
		('CA', 'CAD'),
	]


	Name = models.CharField(max_length=200, default=None,blank=True, null=True) 
	Label = models.CharField(max_length=200, default=None,blank=True, null=True) 
	Currency = models.CharField(
		max_length=2,
		choices=CURRENCY,
		default='CA', blank=True, null=True
	)
	Price = models.FloatField()
	course = models.ForeignKey(Course, default=None,blank=True, null=True, on_delete=models.CASCADE, related_name='pricing')

	def __str__(self):
		return self.Name

class User_Course(models.Model):
	CHOICES = [
		('CO', 'Completed'),
		('ST', 'Started'),
	]

	user = models.ForeignKey(User, on_delete=models.CASCADE)
	course = models.ForeignKey(Course, on_delete=models.CASCADE)
	status = models.CharField(
		max_length=2,
		choices=CHOICES,
		default='ST',
	) 

	def __str__(self):
		return str(self.user) + " - " + str(self.course) + " - " + str(self.status)


class User_Favorited(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	course = models.ForeignKey(Course, on_delete=models.CASCADE)
	def __str__(self):
		return str(self.user) + " - " + str(self.course)


class Course_Credit(models.Model):	
	credit = models.ForeignKey(Credit, on_delete=models.CASCADE)
	course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='courseCredit')
	district = models.ForeignKey(District, default=None,blank=True, null=True, on_delete=models.CASCADE)
	amount = models.PositiveBigIntegerField()

	def __str__(self):
		return str(self.credit) + " - " + str(self.course) + " - " + str(self.amount)