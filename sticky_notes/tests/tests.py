from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from sticky_notes.models import Note
from sticky_notes.forms import NoteForm


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


class NoteViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="emmanuel", password="pass123")
        self.client.login(username="emmanuel", password="pass123")
        self.note = Note.objects.create(title="First", content="Content", owner=self.user)

    def test_list_notes(self):
        response = self.client.get(reverse("note_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "First")

    def test_view_note_detail(self):
        response = self.client.get(reverse("note_detail", args=[self.note.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Content")

    def test_create_note_valid(self):
        response = self.client.post(reverse("note_create"), {
            "title": "New Note",
            "content": "Some text",
        })
        self.assertEqual(response.status_code, 302)  # redirect after success
        self.assertTrue(Note.objects.filter(title="New Note").exists())

    def test_update_note(self):
        response = self.client.post(reverse("note_update", args=[self.note.id]), {
            "title": "Updated",
            "content": "Changed content",
        })
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, "Updated")

    def test_delete_note(self):
        response = self.client.post(reverse("note_delete", args=[self.note.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Note.objects.filter(id=self.note.id).exists())

    def test_view_nonexistent_note(self):
        response = self.client.get(reverse("note_detail", args=[999]))
        self.assertEqual(response.status_code, 404)


class NoteFormTest(TestCase):
    def test_valid_form(self):
        form = NoteForm(data={"title": "Valid", "content": "Content"})
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = NoteForm(data={"title": "", "content": ""})
        self.assertFalse(form.is_valid())
