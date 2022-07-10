"""This module is for an application configurations.
"""
from django.apps import AppConfig

class ContactConfig(AppConfig):
    """An application configuration.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'contact'
