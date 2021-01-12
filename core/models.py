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

class Credit(models.Model):
	credit_type = models.CharField(max_length=200)

	def __str__(self):
		return self.credit_type

class District_Credit(models.Model):
	district = models.ForeignKey(District, on_delete=models.CASCADE)
	credit = models.ForeignKey(Credit, on_delete=models.CASCADE)
	amount = models.PositiveBigIntegerField()

	def __str__(self):
		return str(self.district) + " " + str(self.credit) + " " + str(self.amount)



class Course(models.Model):

	Name = models.CharField(max_length=200)
	Location = models.CharField(max_length=200)
	Price = models.PositiveBigIntegerField()
	Date = models.DateTimeField(blank=True)
	Provider = models.CharField(max_length=200)
	link = models.URLField()

	def __str__(self):
		return self.Name

class User_Course(models.Model):
	CHOICES = [
		('CO', 'Completed'),
		('ST', 'Started'),
	]

	user = models.ForeignKey(User, on_delete=models.CASCADE)
	course = models.ForeignKey(Course, on_delete=models.CASCADE)
	isAdded = models.BooleanField()
	status = models.CharField(
		max_length=2,
		choices=CHOICES,
		default='ST',
	) 



class Course_Credit(models.Model):	
	credit = models.ForeignKey(Credit, on_delete=models.CASCADE)
	course = models.ForeignKey(Course, on_delete=models.CASCADE)
	amount = models.PositiveBigIntegerField()