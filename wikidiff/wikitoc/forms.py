from django import forms
from django.contrib.auth.models import User
from bootstrap_toolkit.widgets import BootstrapDateInput, BootstrapTextInput, BootstrapUneditableInput

class TestForm(forms.Form):
   
    URL = forms.CharField(max_length=100)
   
