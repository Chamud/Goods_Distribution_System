from django.db import models
from django.core.validators import RegexValidator

#Regex
phone_regex = RegexValidator(regex=r'^(\+\d{1,3})?\s?\d{2}\s?\d{3}\s?\d{4,7}$', message="Phone number format: '+94 71 999 9999'")

# Create your models here.
class District(models.Model):
	district_name = models.CharField(max_length=30)

	def __str__(self):
		return self.district_name

class City(models.Model):
	city_name = models.CharField(max_length=30)
	district = models.ForeignKey(District, on_delete=models.CASCADE)

	def __str__(self):
		return self.city_name

class Unit(models.Model):
	unit_name = models.CharField(max_length=10)

	def __str__(self):
		return self.unit_name

class Item(models.Model):
	name = models.CharField(max_length=30)
	description = models.CharField(max_length=200)
	unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
	image = models.ImageField(upload_to='app/items',blank=True, null=True)

	def __str__(self):
		return self.name

class Customer(models.Model):
	name = models.CharField(max_length=30)
	phone_number = models.CharField(validators=[phone_regex], max_length=15)
	city = models.ForeignKey(City, on_delete=models.CASCADE)
	items = models.ManyToManyField(Item, through='Customer_Items')

	def __str__(self):
		return self.name

class Distributor(models.Model):
	name = models.CharField(max_length=30)
	phone_number = models.CharField(validators=[phone_regex], max_length=15)
	image = models.ImageField(upload_to='app/distributors',blank=True, null=True)

	def __str__(self):
		return self.name

class Customer_Items(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
	item = models.ForeignKey(Item, on_delete=models.CASCADE)
	quantity = models.IntegerField()

	def __str__(self):
		return f"{self.customer}_{self.item}"

class Distributor_Items(models.Model):
	distributor = models.ForeignKey(Distributor, on_delete=models.CASCADE)
	item = models.ForeignKey(Item, on_delete=models.CASCADE)
	city = models.ForeignKey(City, on_delete=models.CASCADE)
	quantity = models.IntegerField()

	def __str__(self):
		return f"{self.distributor}_{self.item}_{self.city}"