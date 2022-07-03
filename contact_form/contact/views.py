"""Contact views.
"""
from mailbox import _mboxMMDFMessage
from socket import MsgFlag
from django.core.mail import get_connection
from django.core.mail.message import EmailMultiAlternatives
from django.http import HttpRequest
from django.shortcuts import render
from django.views import View

from .forms import ContactForm
from .models import Bcc, MailSetting
from .exceptions import NeedDBMasterException

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
            form.save()
            customer_email = form.cleaned_data["email"]
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data['message']

            try:
                bcc, setting = self._getSettings()
            except NeedDBMasterException:
                return render(request, 'contact/maintenance.html')

            connection = get_connection()
            mail = EmailMultiAlternatives(
                subject=subject
                , message=message
                , from_email=setting.sender
                , to={customer_email}
                , connection=connection
                , bcc=bcc
            )

            try:
                mail.send()
            except:
                msg = 'Failed to send mail.'
                context = {'form': form, 'error_message': msg}
                return render(request, 'contact/contact.html', context)
            return render(request, 'contact/success.html')
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
