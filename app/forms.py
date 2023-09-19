from django import forms
from django.contrib.auth.models import User
from app.models import *
class signup(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','username','email']
class Companyform(forms.ModelForm):
    class Meta:
        model=Companies
        fields='__all__'