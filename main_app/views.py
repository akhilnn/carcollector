# from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

import uuid
import boto3
from .models import Car, Accessory, Photo
from .forms import ServiceForm

# Constants for boto3
S3_BASE_URL = 'https://s3.us-west-1.amazonaws.com/'
BUCKET = 'carcollector'

# CBV
# Change '__all__' to specify fields
# self.request.user ?
class CarCreate(LoginRequiredMixin, CreateView):
	model = Car
	fields = ['make', 'model', 'year', 'mileage']
	success_url = '/cars/'

	def form_valid(self, form):
		form.instance.user = self.request.user
		return super().form_valid(form)

class CarUpdate(LoginRequiredMixin, UpdateView):
	model = Car
	fields = ['year', 'mileage']

class CarDelete(LoginRequiredMixin, DeleteView):
	model = Car
	success_url = '/cars/'


# Create your views here.
def home(request):
	return render(request, 'home.html')

# render will automatically look inside the templates directory
def about(request):
	return render(request, 'about.html')

@login_required
def cars_index(request):
	cars = Car.objects.filter(user=request.user)
	return render(request, 'cars/index.html', { 'cars': cars })

@login_required
def cars_detail(request, car_id):
	car = Car.objects.get(id=car_id)
	accessories_car_doesnt_have = Accessory.objects.exclude(id__in=car.accessories.all().values_list('id'))
	service_form = ServiceForm()
	return render(request, 'cars/detail.html', { 'car': car, 'service_form': service_form, 'avail_accessories': accessories_car_doesnt_have })

@login_required
def add_service(request, car_id):
	form = ServiceForm(request.POST)
	if form.is_valid():
		new_service = form.save(commit=False)
		new_service.car_id = car_id
		new_service.save()
	return redirect('detail', car_id=car_id)

@login_required
def add_photo(request, car_id):
	# photo-file will be the "name" attribute on the <input type="file">
	photo_file = request.FILES.get('photo-file', None)
	if photo_file:
		s3 = boto3.client('s3')
		# need a unique "key" for S3 / needs image file extension too
		key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
		try:
			s3.upload_fileobj(photo_file, BUCKET, key)
			# build the full url string
			url = f"{S3_BASE_URL}{BUCKET}/{key}"
			# we can assign to car_id or car (if you have a car object)
			photo = Photo(url=url, car_id=car_id)
			photo.save()
		except:
			print('An error occurred uploading file to S3')
	return redirect('detail', car_id=car_id)

@login_required
def assoc_accessory(request, car_id, accessory_id):
	Car.objects.get(id=car_id).accessories.add(accessory_id)
	return redirect('detail', car_id=car_id)

@login_required
def remove_accessory(request, car_id, accessory_id):
	Car.objects.get(id=car_id).accessories.remove(accessory_id)
	return redirect('detail', car_id=car_id)

class AccessoryList(LoginRequiredMixin, ListView):
	model = Accessory

class AccessoryDetail(LoginRequiredMixin, DetailView):
	model = Accessory

class AccessoryCreate(LoginRequiredMixin, CreateView):
	model = Accessory
	fields = '__all__'
	success_url = '/accessories/'

class AccessoryUpdate(LoginRequiredMixin, UpdateView):
	model = Accessory
	fields = ['color']

class AccessoryDelete(LoginRequiredMixin, DeleteView):
	model = Accessory
	success_url = '/accessories/'

def signup(request):
	error_message = ''
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			return redirect('index')
		else:
			error_message = 'Invalid sign up - try again'
	form = UserCreationForm()
	context = {'form': form, 'error_message': error_message}
	return render(request, 'registration/signup.html', context)

