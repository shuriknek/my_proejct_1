 

from django.db import models

class User(models.Model):
    login = models.TextField()
    password = models.TextField()
    
class Session(models.Model):
    key = models.CharField(max_length=200, unique=True)
    user_s = models.ForeignKey(User)
    expires = models.DateTimeField()
    
class ContactForm(models.Model):
    subject = models.TextField()
    message = models.TextField()
    
    def __str__(self):
        return self.name
