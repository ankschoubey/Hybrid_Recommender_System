from django.contrib.auth.models import User
# generic user class we can use

from django import forms

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

# authenticate: take username and password verify that they exist in database
# login: session id: no matter what page you are on you use their id

from django.views.generic import View

class UserForm(forms.ModelForm):
    # make a blueprint to be used while making form

    password = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}))


    class Meta:
        model = User
        # user what information is in User table

        fields = ['username', 'email', 'password']
        # what fields do you want to apear on the form

class LoginForm(forms.ModelForm):
    # make a blueprint to be used while making form

    password = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control'}))

    class Meta:
        model = User
        # user what information is in User table

        fields = ['username', 'password','username']
        # what fields do you want to apear on the form