"""Contact views.
"""
from django.core.mail import get_connection
from django.core.mail.message import EmailMultiAlternatives
from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View

from .forms import ContactForm
from .models import Bcc, Customer, MailSetting
from .exceptions import NeedDBMasterException

def success(request:HttpRequest):
    """The success page to send e-mail.

    Args:
        request (HttpRequest): Request.

    Returns:
        HttpResponse: response.
    """
    return render(request, 'contact/success.html')

class ContactView(View):
    """The view of contact page.
    """
    def get(self, request:HttpRequest):
        """GET.

        Returns:
            HttpResponse: response.
        """
        try:
            self._getSettings()
        except NeedDBMasterException:
            return render(request, 'contact/maintenance.html')
        form = ContactForm()
        context = {'form': form}
        return render(request, 'contact/contact.html', context)

    def post(self, request:HttpRequest):
        """POST.

        Returns:
            HttpResponse: response.
        """
        form = ContactForm(request.POST)
        if form.is_valid():
            customer_name = form.cleaned_data["name"]
            customer_email = form.cleaned_data["email"]
            customer_subject = form.cleaned_data["subject"]
            customer_message = form.cleaned_data['message']

            try:
                bcc, setting = self._getSettings()
            except NeedDBMasterException:
                return render(request, 'contact/maintenance.html')

            subject = self._makeSubject('mail/contact_reply_subject.txt')
            parm = {'name': customer_name, 'subject' : customer_subject, 'message' : customer_message}
            body = self._makeBody('mail/contact_reply_body.txt', parm)

            connection = get_connection()
            mail = EmailMultiAlternatives(
                subject=subject
                , body=body
                , from_email=setting.sender
                , to={customer_email}
                , connection=connection
                , bcc=bcc
            )

            try:
                customer = Customer.objects.get(email=customer_email)
            except Customer.DoesNotExist:
                customer = Customer(name=customer_name, email=customer_email)
            customer.name = customer_name
            customer.count =customer.count + 1

            try:
                mail.send()
            except:
                msg = 'Failed to send mail.'
                context = {'form': form, 'error_message': msg}
                customer.valid = False
                customer.save()
                return render(request, 'contact/contact.html', context)
            form.save()
            customer.save()
            return HttpResponseRedirect(reverse('contact:success'))
        else:
            context = {'form': form}
            return render(request, 'contact/contact.html', context)

    def _getSettings(self):
        """Get Bcc list and the last e-mail setting.

        Raises:
            NeedDBMasterException: Bcc list is zero or email-setting is not found.

        Returns:
            QuerySet: The QuerySet of bcc list.
            MailSetting: The last e-mail setting.
        """
        bcc = Bcc.objects.all()
        setting = MailSetting.objects.filter(enable=True).last()

        if setting is None:
            raise NeedDBMasterException("MailSetting is needed.")
        if len(bcc) == 0:
            raise NeedDBMasterException("Bcc is needed.")

        return bcc, setting

    def _makeBody(self, template:str, context=None):
        """Make a body from a template.

        Args:
            template (str): template name.
            context (Any, optional): template is replaced with the context specified. Defaults to None.

        Returns:
            str: body
        """
        return render_to_string(template, context)

    def _makeSubject(self, template:str, context=None):
        """Make a subject from a template.

        Args:
            template (str): template name.
            context (Any, optional): template is replaced with the context specified. Defaults to None.

        Returns:
            str: subject
        """
        return render_to_string(template, context)
