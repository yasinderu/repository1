from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

def home(request):
	return render(request, 'home.html')

def itinerary(request):
	return render(request, 'Itinerary.html')

def loginView(request):
	context = {
		'page_title': 'LOGIN',
	}

	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(request, username=username, password=password)
		print(user)

		if user is not None:
			login(request, user)

		return redirect('home')

	return render(request, 'login.html', context)

def logoutView(request):
	context = {
		'page_title': 'LOGOUT'
	}

	if request.method == 'POST':
		if request.POST["logout"] == "Submit":
			logout(request)
		return redirect('home')

	return render(request, 'logout.html', context)