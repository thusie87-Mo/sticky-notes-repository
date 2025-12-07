from django.test import TestCase
from django.contrib.auth.models import User
from sticky_notes.models import Note

class NoteFormTest(TestCase):
    def test_valid_form(self):
        form = NoteForm(data={"title": "Valid", "content": "Content"})
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = NoteForm(data={"title": "", "content": ""})
        self.assertFalse(form.is_valid())
