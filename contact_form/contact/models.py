"""This module defines the structure of DB.
"""
from django.db import models

class Customer(models.Model):
    """The model of customer table.
    """
    name = models.CharField('お客様氏名', null=False, blank=False, max_length=100)
    email = models.EmailField('お客様メールアドレス', null=False, blank=False, unique=True)
    newsletter = models.BooleanField('メルマガ希望', null=False, blank=False, default=True)
    valid = models.BooleanField('有効', null=False, blank= False, default=True)
    reject = models.BooleanField('拒否', null=False, blank=False, default=False)
    count = models.IntegerField('問い合わせ回数', null=False, blank=False, default=0)

    class Meta:
        indexes = [
            models.Index(fields=['email'], name='email_idx'),
        ]

    def __str__(self):
        return self.name

class Contact(models.Model):
    """The model of contact table.
    """
    name = models.CharField('お客様氏名', null=False, blank=False, max_length=100)
    email = models.EmailField('お客様メールアドレス', null=False, blank=False)
    subject = models.CharField('件名', null=False, blank=False, max_length=256)
    message = models.TextField('本文', null=False, blank=False)
    time = models.DateTimeField('送信日時', null=False, blank=True)

    def __str__(self):
        return self.email

class Bcc(models.Model):
    """The model of BCC table.
    """
    email = models.EmailField('担当者メールアドレス', null=False, blank=False)
    name = models.CharField('担当者氏名', null=True, blank=True, max_length=100)

    def __str__(self):
        return self.email

class MailSetting(models.Model):
    """The model of mail setting table.
    """
    sender = models.EmailField('送信メールアドレス', null=False, blank=False)
    enable = models.BooleanField('有効', null=False, blank=False, default=True)
