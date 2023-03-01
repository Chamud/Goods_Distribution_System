from django.shortcuts import render, redirect
from app.models import *
from .forms import *
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import datetime
from decouple import config
import itertools
from django.forms.models import model_to_dict

# Create your views here.
def home(request):
	return render(request, 'app/home.html', {'filter':0})

def homefiltered(request, city):
	cityname = City.objects.get(id=city)
	return render(request, 'app/home.html', {'filter': 1, 'city':city, 'search':'', 'cityname':cityname})

def homesearch(request, search):
	return render(request, 'app/home.html', {'filter': 1, 'city':'', 'search':search})

def map(request):
	map_con = config('MAP_CON') #Map connection string
	allInfo = Information.objects.all()
	Infos = [model_to_dict(obj) for obj in allInfo]
	Infos.sort(key=lambda x: x['city'])
	result = {age: list(group) for age, group in itertools.groupby(Infos, key=lambda x: x['city'])}
	allInfo = []
	for key, val in result.items():
		city = City.objects.get(id=key)
		mapInfo = {
			'X' : city.longitude,
			'Y': city.latitude,
			'data' : val,
			'city' : key
		}
		allInfo.append(mapInfo)
	context = { "locate": allInfo, "map_con": map_con}
	return render(request, 'app/map.html', context)

@login_required(login_url='/profile/login')
def post(request, typ, id):
	form = InformationForm()
	provinces = []
	units = []
	provinceid = 0
	districtid = 0
	cityid = 0
	email = ""
	dts = ""
	unitdef = "units"
	qty = 1
	expdt = (datetime.date.today() + datetime.timedelta(30)).strftime("%Y-%m-%d") 

	for province in  Province.objects.all():
		p = { 'id' : province.id, 'name' : province.name }
		provinces.append(p)

	for unit in  Unit.objects.all():
		u = { 'id' : unit.id, 'name' : unit.unit_name }
		units.append(u)

	if id != 0:
		try:
			post = Information.objects.get(id=id)
		except:
			return render(request, 'app/error.html', {'error': "The post couldn't be found" })
		if post.user.user.id != request.user.id:
			return render(request, 'app/error.html', {'error': "Not Accessible" })
		cityid = post.city.id
		districtid = post.city.district.id
		provinceid = post.city.district.province.id
		form = InformationForm(initial={
			'title' : post.title, 
			'description' : post.description, 
			'address' : post.address, 
			'contact' : post.contact, 
			'cityid' : cityid})
		if typ == 1:
			post = Item.objects.get(information=id)
			unitdef = post.unit.unit_name
			qty = post.quantity
			expdate = post.expiary_date.strftime("%Y-%m-%d")
		elif typ == 2:
			post = Service.objects.get(information=id)
			email = post.email
			dts = post.days_times
		else:
			return render(request, 'app/error.html', {'error': "The post couldn't be found" })

	if request.method == 'POST': 
		form = InformationForm(request.POST)
		infoid  = request.POST['infoid']
		typ  = int(request.POST['pors'])
		cityid = int(request.POST['cityid'])
		districtid = int(request.POST['district'])
		provinceid = int(request.POST['province'])
		email = request.POST['email']
		dts = request.POST['datestimes']
		unit = Unit.objects.get(id=request.POST['unit'])
		unitdef = unit.unit_name
		qty = request.POST['amount']
		expdate = request.POST['expdate']
		user = Profile.objects.get(user=request.user)

		if form.is_valid():
			if int(infoid) == 0:
				title 	= form.cleaned_data.get('title')
				desc 	= form.cleaned_data.get('description')
				city 	= City.objects.get(id=form.cleaned_data.get('cityid'))
				contact	= form.cleaned_data.get('contact')
				address	= form.cleaned_data.get('address')
				info 	= Information(title=title, description=desc, address=address, contact=contact, city=city, user=user)
				info.save()
				if typ == 1:
					image	= None
					if 'image' in request.FILES:
						image	= request.FILES['image']
					item	= Item(information=info, unit=unit, image=image, quantity=qty, expiary_date=expdt)
					item.save()
				elif typ == 2:
					service	= Service(information=info, days_times=dts, email=email)
					service.save()
					print('saved')
			else:
				try:
					post = Information.objects.get(id=int(infoid))
				except:
					return render(request, 'app/error.html', {'error': "The post couldn't be found" })
				if post.user.user.id != request.user.id:
					return render(request, 'app/error.html', {'error': "Not Accessible" })
				post.title 		= form.cleaned_data.get('title') 
				post.description= form.cleaned_data.get('description')
				post.address	= form.cleaned_data.get('address')
				post.contact	= form.cleaned_data.get('contact')
				city 	= City.objects.get(id=form.cleaned_data.get('cityid'))
				post.city 		= city
				post.save()
				if typ == 1:
					item = Item.objects.get(information = post)
					image	= None
					if 'image' in request.FILES:
						item.image	= request.FILES['image']
					item.unit = unit
					item.quantity = qty
					item.expiary_date = expdate
					item.save()
				elif typ == 2:
					service = Service.objects.get(information = post)
					service.days_times = dts
					service.email = email
					service.save()
			return redirect(home)
	context = {
		'form' : form,
		'infoid' : id,
		'type' : typ,
		'provinces' : provinces, 
		'units' : units, 
		'provinceid' : provinceid,
		'districtid' : districtid,
		'cityd' : cityid,
		'email' : email,
		'dts' : dts,
		'unitdef' : unitdef,
		'qty' : qty,
		'expdt' : expdt
	}
	return render(request, 'app/post.html', context)


@login_required(login_url='/profile/login')
def deletepost(request, id):
	try:
		post = Information.objects.get(id=id)
	except:
		return render(request, 'app/error.html', {'error': "The post couldn't be found" })
	if post.user.user.id != request.user.id:
		return render(request, 'app/error.html', {'error': "Not Accessible" })
	post.delete()
	return redirect(home)

@login_required(login_url='/profile/login')
def getprofile(request):
	profile = Profile.objects.get(user=request.user)
	profile = getPoints(profile)

	context = {
			'nic': profile.nic,
			'city' : profile.city.name+', '+profile.city.district.name,
			'points' : profile.credibilitypoints
	}
	return render(request, 'app/profile.html', context)

def getPoints(profile):
	profile.credibilitypoints = 0
	infos = Information.objects.filter(user=profile)
	for info in infos:
		rev = Review.objects.filter(information=info)
		for review in rev:
			if review.rate == 1:
				profile.credibilitypoints -= 2
			elif review.rate == 2:
				profile.credibilitypoints -= 1
			elif review.rate == 4:
				profile.credibilitypoints +=1
			elif review.rate == 5:
				profile.credibilitypoints += 2

	#print("cred")
	#print(profile.credibilitypoints)

	rev = Review.objects.filter(user=profile)
	for review in rev:
		revPoints = 0
		#print(review)
		#print(review.rate)
		allReviws = Review.objects.filter(information=review.information)
		for eachreview in allReviws:
			revPoints += eachreview.rate
		if revPoints != 0:
			revPoints = revPoints/len(allReviws)

		#print("avg")
		#print(revPoints)

		diff = abs(review.rate-revPoints)
		#print("diff")
		#print(diff)
		if(diff>=4):
			profile.credibilitypoints -= 1
		elif(diff>=3):
			profile.credibilitypoints -= 0.5
		elif(diff>=2):
			profile.credibilitypoints -= 0.25
		elif(diff>=1):
			profile.credibilitypoints += 0.25
		else:
			profile.credibilitypoints += 0.5

	#print("rev")
	#print(profile.credibilitypoints)
	
	return profile

#def filteredInfo(request, id):
#	items = []
#	return render(request, 'app/allposts.html', {'items' : items })

def filtitems(request, city):
	print("filt items")
	filcityId = city
	print(filcityId)
	items = []
	itemlist = Item.objects.all().order_by('-information')

	for item in itemlist:
		rev = 0
		city = item.information.city
		if city.id!=filcityId:
			continue
		print(item)
		district = city.district
		province = district.province
		allReviws = Review.objects.filter(information=item.information)
		revPoints = 0

		for review in allReviws:
			revPoints += review.rate
		if revPoints != 0:
			revPoints = revPoints/len(allReviws)

		if request.user.is_authenticated:
			try:
				revobj = Review.objects.get(user=Profile.objects.get(user=request.user), information=item.information)
				rev = revobj.rate
			except:
				x=None

		i = {
			'id' 	: item.information.id,
			'itid'	: item.id,
			'title'	: item.information.title,
			'desc' 	: item.information.description,
			'add' 	: item.information.address,
			'cont' 	: item.information.contact,
			'user' 	: item.information.user.user.username,
			'city' 	: city.name,
			'district': district.name,
			'province': province.name,
			'created' : item.information.created_at.strftime("%Y/%m/%d %H:%m"),
			'unit' 	: item.unit,
			'image' : item.image,
			'qty'	: item.quantity,
			'exp'	: item.expiary_date,
			'rev'	: rev,
			'revPoints' : revPoints
		}
		items.append(i)
	return render(request, 'app/itempost.html', {'items' : items, 'filter' : 1})

def items(request, id):
	items = []

	if id == 0:
		itemlist = Item.objects.all().order_by('-information')[:5]
	else:
		itemlist = Item.objects.filter(id__lt=int(id)).order_by('-information')[:5]

	for item in itemlist:
		rev = 0
		city = item.information.city
		district = city.district
		province = district.province
		allReviws = Review.objects.filter(information=item.information)
		revPoints = 0

		for review in allReviws:
			revPoints += review.rate
		if revPoints != 0:
			revPoints = revPoints/len(allReviws)

		if request.user.is_authenticated:
			try:
				revobj = Review.objects.get(user=Profile.objects.get(user=request.user), information=item.information)
				rev = revobj.rate
			except:
				x=None

		i = {
			'id' 	: item.information.id,
			'itid'	: item.id,
			'title'	: item.information.title,
			'desc' 	: item.information.description,
			'add' 	: item.information.address,
			'cont' 	: item.information.contact,
			'user' 	: item.information.user.user.username,
			'city' 	: city.name,
			'district': district.name,
			'province': province.name,
			'created' : item.information.created_at.strftime("%Y/%m/%d %H:%m"),
			'unit' 	: item.unit,
			'image' : item.image,
			'qty'	: item.quantity,
			'exp'	: item.expiary_date,
			'rev'	: rev,
			'revPoints' : revPoints
		}
		items.append(i)
	return render(request, 'app/itempost.html', {'items' : items })

@login_required(login_url='/profile/login')
def review(request, points, info):
	info = Information.objects.get(id=info)
	user = Profile.objects.get(user=request.user)
	try:
		review = Review.objects.get(information=info, user=user)
		review.rate = points
	except: 
		review = Review.objects.create(information=info, user=user, rate=points, comment='-')
	review.save()
	return JsonResponse({'status': 'OK'})


def services(request, id):
	services = []
	if id == 0:
		itemlist = Service.objects.all().order_by('-information')[:5]
	else:
		itemlist = Service.objects.filter(id__lt=int(id)).order_by('-information')[:5]
	for service in itemlist:
		rev = 0
		city = service.information.city
		district = city.district
		province = district.province
		allReviws = Review.objects.filter(information=service.information)
		revPoints = 0

		for review in allReviws:
			revPoints += review.rate

		if revPoints != 0:
			revPoints = revPoints/len(allReviws)

		if request.user.is_authenticated:
			try:
				revobj = Review.objects.get(user=Profile.objects.get(user=request.user), information=item.information)
				rev = revobj.rate
			except:
				x=None

		i = {
			'id' 	: service.information.id,
			'itid'	: service.id,
			'title'	: service.information.title,
			'desc' 	: service.information.description,
			'add' 	: service.information.address,
			'cont' 	: service.information.contact,
			'user' 	: service.information.user.user.username,
			'city' 	: city.name,
			'district': district.name,
			'province': province.name,
			'email'	: service.email,
			'times'	: service.days_times,
			'rev'	: rev,
			'revPoints' : revPoints
		}
		services.append(i)
	return render(request, 'app/servicepost.html', {'items' : services })

def filtservices(request, city):
	filcityId = city
	services = []
	itemlist = Service.objects.all().order_by('-information')
	for service in itemlist:
		rev = 0
		city = service.information.city
		if city.id!=filcityId:
			continue
		print(service)
		district = city.district
		province = district.province
		allReviws = Review.objects.filter(information=service.information)
		revPoints = 0

		for review in allReviws:
			revPoints += review.rate

		if revPoints != 0:
			revPoints = revPoints/len(allReviws)

		if request.user.is_authenticated:
			try:
				revobj = Review.objects.get(user=Profile.objects.get(user=request.user), information=item.information)
				rev = revobj.rate
			except:
				x=None

		i = {
			'id' 	: service.information.id,
			'itid'	: service.id,
			'title'	: service.information.title,
			'desc' 	: service.information.description,
			'add' 	: service.information.address,
			'cont' 	: service.information.contact,
			'user' 	: service.information.user.user.username,
			'city' 	: city.name,
			'district': district.name,
			'province': province.name,
			'email'	: service.email,
			'times'	: service.days_times,
			'rev'	: rev,
			'revPoints' : revPoints
		}
		services.append(i)
	return render(request, 'app/servicepost.html', {'items' : services, 'filter' : 1})

def registration(request):
	form = CreateUserForm()
	provinces = []
	provinceid = 0
	districtid = 0
	cityid = 0
	nic = 0

	for province in  Province.objects.all():
		p = { 'id' : province.id, 'name' : province.name }
		provinces.append(p)

	if request.method == 'POST':
		cityid = int(request.POST['city'])
		districtid = int(request.POST['district'])
		provinceid = int(request.POST['province'])
		if request.user.is_authenticated:
			form = UpdateUserForm(request.POST)
			user = User.objects.get(id=request.user.id)
			profile = Profile.objects.get(user=user)
			nic = profile.nic
			print(form.errors)
			if form.is_valid():
				city = form.cleaned_data.get('city')
				city = City.objects.get(id=city)
				user.first_name = form.cleaned_data.get('first_name')
				user.last_name = form.cleaned_data.get('last_name')
				user.email = form.cleaned_data.get('email')
				user.save()
				profile.city = city
				profile.save()
				return redirect(getprofile)
		else:
			form = CreateUserForm(request.POST)
			if form.is_valid():
				nic = form.cleaned_data.get('nic')
				city = form.cleaned_data.get('city')
				city = City.objects.get(id=city)
				username = form.cleaned_data.get('username')
				form.save()
				user = User.objects.get(username=username)
				profile = Profile.objects.create(user=user, nic=nic, city=city)
				profile.save()
				return redirect(home)
	else:
		if request.user.is_authenticated:
			profile = Profile.objects.get(user=request.user)
			user = profile.user
			city = City.objects.get(id=profile.city.id)
			nic = profile.nic
			provinceid = city.district.province.id
			districtid = city.district.id
			cityid = city.id
			form = CreateUserForm(initial={
					'username' : request.user.username, 
					'email' : user.email, 
					'first_name' : user.first_name, 
					'last_name' : user.last_name, 
					'nic' : profile.nic, 
					'city' : 0
				})
	context = { 
			'form': form, 
			'provinces' : provinces,
			'provinceid' : provinceid,
			'districtid' : districtid,
			'cityd' : cityid,
			'nic' : nic
			}
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
