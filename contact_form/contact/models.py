import email
from email import message
from django.db import models

class Contact(models.Model):
    email = models.EmailField()
    subject = models.CharField(max_length=256)
    message = models.TextField()

    def __str__(self):
        return self.email
