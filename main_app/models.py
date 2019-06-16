from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

CATEGORIES = (
	('R', 'Routine'),
	('S', 'Safety Recall'),
	('N', 'Non-safety Recall'),
	('D', 'Damage Repair')
)

# Create your models here.
# Can subclass here if desired
class Accessory(models.Model):
	name = models.CharField(max_length=50)
	color = models.CharField(max_length=20)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('accessories_detail', kwargs={'pk': self.id})


class Car(models.Model):
	make = models.CharField(max_length=100)
	model = models.CharField(max_length=100)
	year = models.IntegerField()
	mileage = models.IntegerField()
	accessories = models.ManyToManyField(Accessory)
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return f'{self.year} {self.make} {self.model}'

	def get_absolute_url(self):
		return reverse('detail', kwargs={'car_id': self.id})

	def serviced_for_today(self):
		return self.service_set.filter(date=date.today()).count() > 0

	class Meta:
		ordering = ['-year']


class Service(models.Model):
	date = models.DateField()
	category = models.CharField(
		max_length=1,
		choices=CATEGORIES,
		default=CATEGORIES[0][0]
		)
	car = models.ForeignKey(Car, on_delete=models.CASCADE)

	def __str__(self):
		return f'{self.get_category_display()} service completed on {self.date}'

	class Meta:
		ordering = ['-date']


class Photo(models.Model):
	url = models.CharField(max_length=200)
	car = models.ForeignKey(Car, on_delete=models.CASCADE)

	def __str__(self):
		return f"Photo for car_id: {self.car_id} @{self.url}"

