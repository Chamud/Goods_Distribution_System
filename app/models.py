from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
import pytz
from django.utils import timezone

# Create your models here.
class Province(models.Model):
	name = models.CharField(max_length=30)

	def __str__(self):
		return self.name

class District(models.Model):
	name = models.CharField(max_length=30)
	province = models.ForeignKey(Province, on_delete=models.CASCADE)

	def __str__(self):
		return self.name

class City(models.Model):
	name = models.CharField(max_length=30)
	postal_code = models.CharField(max_length=5)
	longitude = models.FloatField()
	latitude = models.FloatField()
	district = models.ForeignKey(District, on_delete=models.CASCADE)

	def __str__(self):
		return self.name

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	nic = models.CharField(max_length=15, unique=True)
	credibilitypoints = models.IntegerField(default=0)
	city = models.ForeignKey(City, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.user)

class Tag(models.Model):
	tag_name = models.CharField(max_length=15, unique=True)

	def __str__(self):
		return self.tag_name

class Information(models.Model):
	title = models.CharField(max_length=100)
	description = models.TextField()
	address = models.TextField()
	contact = models.CharField(max_length=15)
	user = models.ForeignKey(Profile, on_delete=models.CASCADE)
	city = models.ForeignKey(City, on_delete=models.CASCADE)
	created_at = models.DateTimeField(default=timezone.now, editable=False)
	tags = models.ManyToManyField(Tag, through='Information_Tags')

	def __str__(self):
		return f"{convert_to_localtime(self.created_at)}_{self.title}"

class Information_Tags(models.Model):
	information =  models.ForeignKey(Information, on_delete=models.CASCADE)
	tag =  models.ForeignKey(Tag, on_delete=models.CASCADE)

	class Meta:
		unique_together = ('information', 'tag')

	def __str__(self):
		return f"{self.information.title}_{self.tag}"

class Unit(models.Model):
	unit_name = models.CharField(max_length=10, unique=True)

	def __str__(self):
		return self.unit_name

class Item(models.Model):
	information =  models.OneToOneField(Information, on_delete=models.CASCADE)
	unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
	image = models.ImageField(upload_to='items',blank=True, null=True)
	quantity = models.IntegerField()
	expiary_date = models.DateField()

	def __str__(self):
		return f"IS_{self.information.title}"

class Service(models.Model):
	information =  models.OneToOneField(Information, on_delete=models.CASCADE)
	days_times = models.TextField()
	email = models.EmailField()

	def __str__(self):
		return f"IS_{self.information.title}"


class Review(models.Model):
	user = models.ForeignKey(Profile, on_delete=models.CASCADE)
	information =  models.ForeignKey(Information, on_delete=models.CASCADE)
	rate = models.IntegerField()
	comment = models.TextField()


	def __str__(self):
		return f"{str(self.user.user)}_on_{self.information.title}"

def convert_to_localtime(utctime):
	fmt = '%Y.%m.%d_%H.%M'
	utc = utctime.replace(tzinfo=pytz.UTC)
	localtz = utc.astimezone(pytz.timezone('Asia/Colombo'))
	return localtz.strftime(fmt)