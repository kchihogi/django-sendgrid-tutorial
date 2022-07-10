from django.forms import ModelForm
from django.utils import timezone
from .models import Contact

class ContactForm(ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'

    def save(self, commit=True):
        obj = super(ContactForm, self).save(commit=False)
        obj.time = timezone.now()
        if commit:
            obj.save()
        return obj
