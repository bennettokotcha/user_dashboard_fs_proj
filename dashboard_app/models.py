from django.db import models
import re

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['first_name']) < 2:
            errors['first_name'] = 'Provided FIRST NAME must be at least 2 characters.'
        if len(postData['last_name']) < 2:
            errors['last_name'] = 'Provided LAST NAME must be at least 2 characters.'
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address."
        if len(postData['password']) < 8:
            errors['password'] = 'Provided PASSWORD must be at least 8 characters.'
        if postData['confirm_pw'] != postData['password']:
            errors['confirm_pw'] = 'Passwords do not match!'
        return errors

    def login_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address."
        if len(postData['password']) < 8:
            errors['password'] = 'Provided PASSWORD must be at least 8 characters.'
        return errors

    def info_edit_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address."
        if len(postData['first_name']) < 2:
            errors['first_name'] = 'Provided FIRST NAME must be at least 2 characters.'
        if len(postData['last_name']) < 2:
            errors['last_name'] = 'Provided LAST NAME must be at least 2 characters.'
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address."
        # if len(postData['password']) < 8:
        #     errors['password'] = 'Provided PASSWORD must be at least 8 characters.'
        # if postData['confirm_pw'] != postData['password']:
        #     errors['confirm_pw'] = 'Passwords do not match!'
        return errors

    def password_edit_validator(self, postData):
        errors = {}
        if len(postData['password']) < 8:
            errors['password'] = 'Provided PASSWORD must be at least 8 characters.'
        if postData['confirm_pw'] != postData['password']:
            errors['confirm_pw'] = 'Passwords do not match!'
        return errors
    

    #users_created = []

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=275)
    desc = models.CharField(max_length=300, null=True)
    user_level = models.BooleanField()
    password = models.CharField(max_length=75)
    confirm_pw = models.CharField(max_length=75)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    # added_posts = []
    # posts_made = []
    # comments_made = []

class Post(models.Model):
    added_to = models.ForeignKey(User, related_name='added_posts', on_delete=models.CASCADE, null=True)
    posted_by = models.ForeignKey(User, related_name='posts_made', on_delete=models.CASCADE)
    message = models.CharField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # messages_made = []

class Comment(models.Model):
    comment = models.CharField(max_length=140)
    posted_by = models.ForeignKey(User, related_name='comments_made', on_delete=models.CASCADE)
    message = models.ForeignKey(Post, related_name='messages_made', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# Create your models here.
