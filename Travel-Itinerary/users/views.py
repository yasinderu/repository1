from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.views import View
from django.contrib import messages

# Create your views here.

class Users(View):
	template_name = 'users/register.html'
	form = UserCreationForm()
	context = {
		'form': form
	}

	def get(self, request):
		return render(request, self.template_name, self.context)

	def post(self, request):
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Account created for {username}!')
			return redirect('home')
		return render(request, self.template_name, self.context)
