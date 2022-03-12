from re import I
from django.forms import forms
from django.test import TestCase
from bookmark.forms import ImageCreateForm



class BookmarkModelTest(TestCase):

    def test_form_invalid_url(self):
        form = ImageCreateForm(data={'title':'test','url':'example.com/pic.kmv','description':'test'})
        self.assertFalse(form.is_valid())

    def test_form_valid_url(self):
        form = ImageCreateForm(data={'title':'test','url':'example.com/pic.jpg','description':'test'})
        self.assertTrue(form.is_valid())
        form.fields['url'] = 'example.com/pic.jpeg'
        self.assertTrue(form.is_valid())