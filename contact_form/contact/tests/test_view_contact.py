"""UT Test module for the Contact View
"""
from django.test import TestCase
from django.urls import reverse

from initial_data import master_data

class ContactViewTest(TestCase):
    """This class is an object to test the ContactView."""

    def test_no_main_setting_and_bcc(self):
        """If no MailSetting and BCC resistered, the maintenace page is returned.
        """
        response = self.client.get(reverse('contact:contact'))
        self.assertContains(response=response, text='Maintenance')

    def test_no_bcc(self):
        """If no BCC resistered, the maintenace page is returned.
        """
        master_data.add_mail_setting()
        master_data.add_mail_setting()
        response = self.client.get(reverse('contact:contact'))
        self.assertContains(response=response, text='Maintenance')

    def test_no_main_setting(self):
        """If no MailSetting resistered, the maintenace page is returned.
        """
        master_data.add_bcc()
        master_data.add_bcc()
        response = self.client.get(reverse('contact:contact'))
        self.assertContains(response=response, text='Maintenance')
