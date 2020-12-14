from django import forms


class SearchForm(forms.Form):
    location = forms.CharField(max_length=30)
    category = forms.CharField(max_length=30)
    price = forms.ChoiceField(choices=[(1, "$"), (2, "$$"), (3, "$$$"), (4, "$$$$")])
    hours = forms.ChoiceField(choices=[(True, "Open Now"), (False, "No Preference")])
