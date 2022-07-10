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

    def save(self, commit=True):
        """a orverride method for the save method.

        Args:
            commit (bool, optional): commit flag. If not, it will not save.Defaults to True.

        Returns:
            Contact: the obejct of Contact.
        """
        super().__init__(ContactForm, self).save(commit=False)
        obj = super(ContactForm, self).save(commit=False)
        obj.time = timezone.now()
        if commit:
            obj.save()
        return obj
