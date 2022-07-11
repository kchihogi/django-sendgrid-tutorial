"""This module defines the form.
"""
from django.forms import ModelForm
from django.utils import timezone
from .models import Contact

class ContactForm(ModelForm):
    """The model form of the contact table.
    """
    class Meta:
        model = Contact
        fields = '__all__'

    def save(self, *args, **kwargs):
        """a orverride method for the save method.

        Returns:
            Contact: the obejct of Contact.
        """
        obj = super().save(commit=False)
        obj.time = timezone.now()
        obj.save(args,kwargs)
        return obj
