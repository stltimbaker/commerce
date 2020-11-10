from django import forms
#from django.forms import modelform_factory

from .models import Listing

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['itemName','itemShortDescription','itemLongDescription','setPrice','category','imageURL']
