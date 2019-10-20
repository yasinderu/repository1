from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from users.forms import RegisForm, EditForm
from django.views import View
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

class Users(View):
	template_name = 'users/register.html'
	form = RegisForm()
	context = {
		'page_title': 'Register',
		'form': form,
	}
	def get(self, request):
		return render(request, self.template_name, self.context)

	def post(self, request):
		form = RegisForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Account created for {username}!')

			return redirect('login')
		else:
			print(form)
		return render(request, self.template_name, self.context)

def loginView(request):
	context = {
		'page_title': 'LOGIN',
	}

	user = None

	if request.method == 'GET':
		if request.user.is_authenticated:
			return redirect('home')
		else:
			return render(request, 'login.html', context)

	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(request, username=username, password=password)
		#print(user)

		if user is not None:
			login(request, user)

		return redirect('view_profile')

@login_required
def logoutView(request):
	context = {
		'page_title': 'LOGOUT'
	}

	if request.method == 'POST':
		if request.POST["logout"] == "Submit":
			logout(request)
		return redirect('home')

	return render(request, 'logout.html', context)

@login_required
def view_profile(request):
	template_name = 'users/profile.html'
	context = {
		'user': request.user
	}
	return render(request, template_name, context)

@login_required
def edit_profile(request):
	template_name = 'users/edit.html'
	if request.method == 'POST':
		form = EditForm(request.POST, instance=request.user)
		if form.is_valid():
			form.save()
			return redirect('view_profile')
	else:
		form = EditForm(instance=request.user)
		context = {
			'page_title': 'EDIT PROFILE',
			'form': form,
		}
		return render(request, template_name, context)