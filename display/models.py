from django.db import models
import datetime
from django.utils import timezone
from django import forms

class InputBox (forms.Form):
    station1 = forms.CharField(label= 'Station 1 ',max_length=4)
    w_normal1 = forms.BooleanField(required=False)
    station2 = forms.CharField(label= 'Station 2 ', max_length=4, required=False)
    w_normal2 = forms.BooleanField(required=False)
    station3 = forms.CharField(label= 'Station 3 ', max_length=4, required=False)
    w_normal3 = forms.BooleanField(required=False)
    year = forms.CharField(label= 'Year ', max_length=4)
