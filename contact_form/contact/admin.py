"""This module set up the admin page of django site.
"""
from django.contrib import admin
from .models import Bcc, Contact, Customer, MailSetting

admin.site.register(Customer)
admin.site.register(Contact)
admin.site.register(Bcc)
admin.site.register(MailSetting)
