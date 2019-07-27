from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
import bcrypt
import re
 
from .models import *
# Create your views here.
def index(request):

    return render (request, "log_reg_attack_app/index.html")

def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        context = {
            "log_user": User.objects.get(id=request.session['user_id'])
        }
        return render(request,"attack_app/attack.html", context)

def register(request):
    errors = User.objects.new_user_validator(request.POST)
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/')
    else:
        hash_password = User.objects.give_new_user_password(request.POST['password'])
        new_user = User.objects.create(birthday = request.POST['bday'])
        new_user.first_name = request.POST['first_name']
        new_user.last_name = request.POST["last_name"]
        new_user.alias = request.POST["alias"]
        new_user.email = request.POST["email"]
        new_user.password = hash_password
        new_user.save()
        new_user_id = new_user.id
        request.session['user_id'] = new_user.id
        return redirect('/pirates_attack')


def login(request):
    errors = User.objects.login_user_validator(request.POST)
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/')
    else:
        request.session['user_id'] = User.objects.get(email=request.POST['email']).id
        return redirect('/pirates_attack')    

def logout(request):
    request.session.clear()
    return redirect('/')
