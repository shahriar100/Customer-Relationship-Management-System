from django.forms import ModelForm
from .models import *
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__' # ['customer', 'product'] # in case of selecting individually

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user'] #customer will not be able to update user field


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class  CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
