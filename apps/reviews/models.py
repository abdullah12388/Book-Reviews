from __future__ import unicode_literals

from django.db import models

# Create your models here.
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if (len(postData['name']) < 1) or (len(postData['email']) < 1):
            errors["blank"] = "All fields are required and must not be blank!"
        if not (postData['name'].isalpha():
            errors["alpha"] = "Name cannot contain any numbers!"
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"] = "Invalid Email Address!"
        return errors


class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    #uploaded_books = models.ForeignKey(Book, related_name = "uploader", null=True)
    #liked_books = models.ManyToManyField(Book, related_name="liked_users", null=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()

    def __unicode__(self):
        return "id: " + str(self.id) + "first_name: " + self.first_name + "last_name: " + self.last_name

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    uploader = models.ForeignKey(User, related_name = "uploaded_books", null=True)
    reviewed_users = models.ManyToManyField(User, related_name="reviewed_books", null=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __unicode__(self):
        return "id: " + str(self.id) + "title: " + self.title + "author: " + self.author

class Review(models.Model):
    review = models.TextField()
    book_id = models.ForeignKey(Book, related_name = "reviewes", null=True)
    user_id = models.ForeignKey(User, related_name = "posted_reviews", null=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

def __unicode__(self):
    return "id: " + str(self.id) + "review: " + self.title + "created_at: " + self.created_at