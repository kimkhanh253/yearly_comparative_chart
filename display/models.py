from django.db import models
import datetime
from django.utils import timezone
from django import forms

class InputBox (forms.Form):
    year = forms.CharField(max_length=4)
    station1 = forms.CharField(max_length=4)
    station2 = forms.CharField(max_length=4)
    w_normal = forms.BooleanField(required=False)
    
