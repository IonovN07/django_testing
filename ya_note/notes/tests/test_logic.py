from http import HTTPStatus

from pytils.translit import slugify

from notes.models import Note
from notes.forms import WARNING
from .testing_utils import (
    ADD_URL,
    DELETE_NOTE_URL,
    EDIT_NOTE_URL,
    REDIRECT_ADD_URL,
    BaseTest
)


class TestLogic(BaseTest):

    def test_not_unique_slug(self):
        existing_notes = set(Note.objects.all())
        self.note_data['slug'] = self.note.slug
        self.assertFormError(
            self.author_client.post(ADD_URL, data=self.note_data),
            'form',
            'slug',
            errors=(self.note.slug + WARNING)
        )
        self.assertEqual(existing_notes, set(Note.objects.all()))

    def test_slug_is_auto_generated_when_not_provided(self):
        self.note_data.pop('slug')
        notes = set(Note.objects.all())
        self.assertEqual(
            self.author_client.post(
                ADD_URL, data=self.note_data
            ).status_code,
            HTTPStatus.FOUND
        )
        notes = set(Note.objects.all()) - notes
        self.assertEqual(len(notes), 1)
        note = notes.pop()
        self.assertEqual(note.slug, slugify(self.note_data['title']))
        self.assertEqual(note.title, self.note_data['title'])
        self.assertEqual(note.text, self.note_data['text'])
        self.assertEqual(note.author, self.author)

    def test_logged_in_user_can_create_note(self):
        notes = set(Note.objects.all())
        self.assertEqual(
            self.author_client.post(ADD_URL, self.note_data).status_code,
            HTTPStatus.FOUND
        )
        notes = set(Note.objects.all()) - notes
        self.assertEqual(len(notes), 1)
        note = notes.pop()
        self.assertEqual(note.title, self.note_data['title'])
        self.assertEqual(note.text, self.note_data['text'])
        self.assertEqual(note.slug, self.note_data['slug'])
        self.assertEqual(note.author, self.author)

    def test_anonym_user_cant_create_note(self):
        notes = set(Note.objects.all())
        responce = self.client.post(ADD_URL, self.note_data)
        self.assertEqual(
            responce.status_code,
            HTTPStatus.FOUND
        )
        self.assertRedirects(responce, REDIRECT_ADD_URL)
        self.assertEqual(notes, set(Note.objects.all()))

    def test_not_author_cannot_delete_note(self):
        notes = set(Note.objects.all())
        self.assertEqual(
            self.not_author_client.post(DELETE_NOTE_URL).status_code,
            HTTPStatus.NOT_FOUND
        )
        self.assertEqual(notes, set(Note.objects.all()))
        note = Note.objects.get(id=self.note.id)
        self.assertEqual(note.title, self.note.title)
        self.assertEqual(note.text, self.note.text)
        self.assertEqual(note.slug, self.note.slug)
        self.assertEqual(note.author, self.note.author)

    def test_not_author_cannot_edit_note(self):
        self.assertEqual(
            self.not_author_client.post(EDIT_NOTE_URL).status_code,
            HTTPStatus.NOT_FOUND
        )
        note = Note.objects.get(id=self.note.id)
        self.assertEqual(note.title, self.note.title)
        self.assertEqual(note.text, self.note.text)
        self.assertEqual(note.slug, self.note.slug)
        self.assertEqual(note.author, self.note.author)

    def test_author_can_edit_note(self):
        self.assertEqual(
            self.author_client.post(
                EDIT_NOTE_URL, data=self.note_data
            ).status_code,
            HTTPStatus.FOUND
        )
        note = Note.objects.get(id=self.note.id)
        self.assertEqual(note.title, self.note_data['title'])
        self.assertEqual(note.text, self.note_data['text'])
        self.assertEqual(note.slug, self.note_data['slug'])
        self.assertEqual(note.author, self.note.author)

    def test_author_can_delete_note(self):
        self.assertEqual(
            self.author_client.post(DELETE_NOTE_URL).status_code,
            HTTPStatus.FOUND
        )
        self.assertFalse(Note.objects.filter(id=self.note.id).exists())
