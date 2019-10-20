from django.shortcuts import render, redirect

def home(request):
	context = {
		'page_title': 'HOME',
	}
	return render(request, 'home.html', context)