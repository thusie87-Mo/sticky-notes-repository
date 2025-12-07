from django.test import TestCase
from django.contrib.auth.models import User
from notes.models import Note

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
