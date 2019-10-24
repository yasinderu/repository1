from django import forms

class itineraryForm(forms.Form):
	from_places = forms.CharField(label='Origin', max_length=100)
	to_places = forms.CharField(label='Destination', max_length=100)