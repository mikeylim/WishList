# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re, bcrypt
from django.db import models
from datetime import datetime  

# Create your models here.
class ValidateManager(models.Manager):
    def register(self, postData):
        errorMessages = []
        if len(postData["name"]) < 1 or len(postData['username']) < 1 or len(postData['password']) < 1 or len(postData['confirm']) < 1 or len(postData['date_hired']) < 1:
            errorMessages.append("All fields must not be blank")  
        else:                
            if postData["name"].isdigit():
                errorMessages.append("Name cannot contain any numbers")

            if len(postData['name']) < 3:
                errorMessages.append("Name has to be at least 3 chracters")

            if len(postData['username']) < 3:
                errorMessages.append("Username has to be at least 3 chracters")

            if postData['username'].isdigit():
                errorMessages.append('Username name cannot contain any numbers')

            if postData['password'] != postData['confirm']:
                errorMessages.append('Password and Password Confirmation do not match')

            if len(postData['password']) < 8:
                errorMessages.append('Password must be at least 8 characters long')

            try:
                y, m, d = map(int, postData['date_hired'].split('-'))
                date_hired = datetime(y, m, d)
                if date_hired > datetime.now():
                    errorMessages.append('Date Hired must be before today')
            except:
                errorMessages.append('Please enter date field')

            if len(errorMessages) == 0:
                hashpw = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
                newUser = User.objects.create(name=postData['name'], username=postData['username'], password=hashpw, date_hired=date_hired)
                return newUser       
        return errorMessages

    def login(self, postData):
        errorMessages = []
        # try:
        user = User.objects.get(username=postData['username'])
        if bcrypt.hashpw(postData['password'].encode(), user.password.encode()) == user.password.encode():
            return user
        else:
            errorMessages.append('Invalid password')
            return errorMessages
        # except:
        #     # errorMessages.append('No user registered with that username')
        #     return errorMessages
class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    date_hired = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ValidateManager()
    def __str__(self):
        return self.name + " " + self.username