from django import forms


class RestaurantForm(forms.Form):
    name = forms.CharField(label="Restaurant Name")
    email = forms.EmailField(label="Email")
    ownername = forms.CharField(label="Owner Name")
    description = forms.CharField(label="Description")
    username = forms.CharField(label="Username")
