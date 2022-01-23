from tkinter import Widget
from django import forms
import django_filters
from .models import *


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields =[ 'vehicaltype','manufacturer', 'vmodel', 'myear','category']


