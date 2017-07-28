from __future__ import unicode_literals
from django.db import models
import re
# from datetime import datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validate_reg(self, post_data):
        errors = {}
        if len(post_data['name']) < 3:
            errors['name'] = "Name must be at least 3 characters long"
        if len(post_data['alias']) < 2:
            errors['alias'] = "Alias must be at least 2 characters long"
        if not re.match(EMAIL_REGEX, post_data['email']):
            errors['email'] = "Email must be of correct format."
        if len(post_data['password']) < 8:
            errors['password'] = "Password must be at least 8 characters long"
        if post_data['password'] != post_data['confirm_pw']:
            errors['password'] = "Password must match password confirmation field"
        if len(post_data['birthdate']) < 2:
            errors['birthdate'] = "Please enter a birthdate"
        # if datetime.strptime(post_data['birthdate'], '%Y-%m-%d').date() < datetime.now().date():
        #     errors['birthdate'] = "Error! Current date or future date."
        print errors
        return errors

class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    birthdate = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Poke(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    poker = models.ForeignKey(User, related_name = "pokes_made")
    pokee = models.ForeignKey(User, related_name = "pokes_received")