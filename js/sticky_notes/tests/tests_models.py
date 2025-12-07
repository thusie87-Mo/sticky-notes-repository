from django.test import TestCase
from django.contrib.auth.models import User
from notes.models import Note

class NoteModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="emmanuel", password="pass123")

    def test_create_note(self):
        note = Note.objects.create(title="Test Note", content="Hello world", owner=self.user)
        self.assertEqual(note.title, "Test Note")
        self.assertEqual(note.owner.username, "emmanuel")

    def test_str_representation(self):
        note = Note.objects.create(title="Sticky", content="Content", owner=self.user)
        self.assertEqual(str(note), "Sticky")
