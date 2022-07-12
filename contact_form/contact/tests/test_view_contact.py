"""UT Test module for the Contact View
"""
from django.test import TestCase
from django.urls import reverse

class ContactViewTest(TestCase):
    """This class is an object to test the ContactView."""

    def test_no_profile(self):
        """If no profile resistered, the about page returns 404.
        """
        response = self.client.get(reverse('contact:contact'))
        self.assertContains(response=response, text='Maintenance')
