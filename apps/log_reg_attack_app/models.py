from __future__ import unicode_literals
from django.db import models
from datetime import datetime, timedelta
import bcrypt
import re


class LoginManager(models.Manager):
    def new_user_validator(self, postData):
        errors = {}
        user = User.objects.filter(email=postData['email'])
        # add keys and values to errors dictionary for each invalid field
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should be at least 2 characters"
        elif len(postData['last_name']) < 2:
            errors["last_name"] = "Last name should be at least 2 characters"
        elif not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", postData['email']):
            errors['email'] = "Please enter valid email address"
        elif user:
            errors['email']="Email already in use"
        elif len(postData['password']) < 3:
            errors["password"] = "Password should be at least 3 characters"
        elif postData['password'] != postData['confirmation_password']:
            errors['password'] = "Passwords must match"
        return errors

    def give_new_user_password(self, password):
        hash1 = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        return hash1

    def login_user_validator(self, postData):
        errors={}
        if len(postData['email'])==0:
            errors["email"] = "Please enter a valid email"

        user = User.objects.filter(email=postData['email'])
        if not user:
            errors["email"] = "Email not found"
 
        else:
            if len(postData['password']) ==0:
                errors["password"] = "Please enter a password."
            elif bcrypt.checkpw(postData['password'].encode(), user[0].password.encode()):
                print("password match")
            else:
                print("failed password")
                errors['password'] = "Password fails"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    alias = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    birthday = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = LoginManager()



