"""Contact views.
"""
from smtplib import SMTPException

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
            self._get_settings()
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
            try:
                self._send_mail(form)
            except NeedDBMasterException:
                return render(request, 'contact/maintenance.html')
            except SMTPException:
                msg = 'Failed to send mail.'
                context = {'form': form, 'error_message': msg}
                return render(request, 'contact/contact.html', context)
            form.save()
            self._save_customer_info(form)
            return HttpResponseRedirect(reverse('contact:success'))
        context = {'form': form}
        return render(request, 'contact/contact.html', context)

    def _get_settings(self):
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

    def _send_mail(self, form:ContactForm):
        """Send e-mail of the contact form.

        Raises:
            NeedDBMasterException: Bcc list is zero or email-setting is not found.
            SMTPException: An error to send e-mail.

        Args:
            form (ContactForm): The model form of the contact table.
        """
        # prep
        bcc, setting = self._get_settings()

        # make
        subject = render_to_string('mail/contact_reply_subject.txt')
        parm = {'name': form.cleaned_data["name"]
        , 'subject' : form.cleaned_data["subject"]
        , 'message' : form.cleaned_data['message']
        }
        body = render_to_string('mail/contact_reply_body.txt', parm)

        # send
        connection = get_connection()
        mail = EmailMultiAlternatives(
            subject=subject
            , body=body
            , from_email=setting.sender
            , to={form.cleaned_data["email"]}
            , connection=connection
            , bcc=bcc
        )
        mail.send()

    def _save_customer_info(self, form:ContactForm):
        """save the customer info with grouping by e-mail.

        Args:
            form (ContactForm): The model form of the contact table.
        """
        customer_name = form.cleaned_data["name"]
        customer_email = form.cleaned_data["email"]
        try:
            customer = Customer.objects.get(email=customer_email)
        except Customer.DoesNotExist:
            customer = Customer(name=customer_name, email=customer_email)
        customer.name = customer_name
        customer.count =customer.count + 1
        customer.save()
