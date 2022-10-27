from django.shortcuts import render, redirect
from app.models import *
from .forms import *
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import datetime

# Create your views here.
def home(request):
	return render(request, 'app/home.html')

def map(request):
	return render(request, 'app/map.html')

@login_required(login_url='/profile/login')
def post(request):
	form = InformationForm()
	provinces = []
	units = []
	expdt = datetime.date.today() + datetime.timedelta(30)
	for province in  Province.objects.all():
		p = { 'id' : province.id, 'name' : province.name }
		provinces.append(p)

	for unit in  Unit.objects.all():
		u = { 'id' : unit.id, 'name' : unit.unit_name }
		units.append(u)

	if request.method == 'POST':
		form = InformationForm(request.POST)
		if form.is_valid():
			print(form.cleaned_data.get('title'))
			return redirect(home)
	context = { 'form': form, 'provinces' : provinces, 'units' : units, 'expdt' : expdt.strftime("%Y-%m-%d") }
	return render(request, 'app/post.html', context)

@login_required(login_url='/profile/login')
def profile(request):
	return render(request, 'app/profile.html')

def registration(request):
	form = CreateUserForm()
	provinces = []
	for province in  Province.objects.all():
		p = { 'id' : province.id, 'name' : province.name }
		provinces.append(p)

	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			nic = form.cleaned_data.get('nic')
			city = form.cleaned_data.get('city')
			user = User.objects.get(username=username)
			city = City.objects.get(id=city)
			profile = Profile.objects.create(user=user, nic=nic, city=city)

	context = { 'form': form, 'provinces' : provinces}
	return render(request, 'app/registration.html', context)

def loginUser(request):
	error = ''
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect(home)
		else:
			error = 'Username or password is incorrect'
	return render(request, 'app/login.html', {'error' : error})

def logoutUser(request):
	logout(request)
	return redirect(home)

def getdistricts(request, id):
	province = Province.objects.get(id=id)
	districts = []
	for district in District.objects.order_by('name').filter(province=province):
		d = { 'id' : district.id, 'name' : district.name }
		districts.append(d)
	return JsonResponse({'context': districts})

def getcities(request, id):
	district = District.objects.get(id=id)
	cities = []
	for city in City.objects.order_by('name').filter(district=district):
		d = { 'id' : city.id, 'name' : city.name }
		cities.append(d)
	return JsonResponse({'context': cities})

