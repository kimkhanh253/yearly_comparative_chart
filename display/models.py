from django.db import models
import datetime
from django.utils import timezone
from django import forms

class InputBox (forms.Form):
    year = forms.CharField(max_length=4)
    station1 = forms.CharField(max_length=4)
    w_normal1 = forms.BooleanField(required=False)
    station2 = forms.CharField(max_length=4, required=False)
    w_normal2 = forms.BooleanField(required=False)
    station3 = forms.CharField(max_length=4, required=False)
    w_normal3 = forms.BooleanField(required=False)
    
