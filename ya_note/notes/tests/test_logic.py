from http import HTTPStatus

from pytils.translit import slugify

from notes.models import Note
from notes.forms import WARNING
from .testing_utils import (
    ADD_URL,
    LOGIN_URL,
    DELETE_NOTE_URL,
    EDIT_NOTE_URL,
    REDIRECT_ADD_URL,
    BaseTest
)


class TestLogic(BaseTest):

    def test_not_unique_slug(self):
        notes_before = set(Note.objects.all()) # привести к единой переменной
        self.note_data['slug'] = self.note.slug
        self.assertFormError(
            self.author_client.post(ADD_URL, data=self.note_data),
            'form',
            'slug',
            errors=(self.note.slug + WARNING)
        )
        self.assertEqual(notes_before, set(Note.objects.all()))

    def test_slug_is_auto_generated_when_not_provided(self):
        self.note_data.pop('slug')
        existing_notes = set(Note.objects.all())
        self.assertEqual(
            self.author_client.post(
                ADD_URL, data=self.note_data
            ).status_code,
            302
        )
        new_notes = set(Note.objects.all())
        created_notes = new_notes - existing_notes
        self.assertEqual(len(created_notes), 1)
        new_note = created_notes.pop()
        self.assertEqual(new_note.slug, slugify(self.note_data['title']))
        self.assertEqual(new_note.title, self.note_data['title'])
        self.assertEqual(new_note.text, self.note_data['text'])
        self.assertEqual(new_note.author, self.author)

    def test_user_can_create_note(self):
        existing_notes = set(Note.objects.all())
        self.assertEqual(
            self.author_client.post(ADD_URL, self.note_data).status_code,
            302
        )
        new_notes = set(Note.objects.all())
        created_notes = new_notes - existing_notes
        self.assertEqual(len(created_notes), 1)
        new_note = created_notes.pop()
        self.assertEqual(new_note.title, self.note_data['title'])
        self.assertEqual(new_note.text, self.note_data['text'])
        self.assertEqual(new_note.slug, self.note_data['slug'])
        self.assertEqual(new_note.author, self.author)

    def test_anonymous_user_cant_create_note(self):
        notes_before = set(Note.objects.all())
        responce = self.client.post(ADD_URL, self.note_data)
        self.assertEqual(responce.status_code, 302)
        self.assertRedirects(responce, REDIRECT_ADD_URL)
        self.assertEqual(notes_before, set(Note.objects.all()))

    def test_not_author_cannot_delete_note(self):
        notes_before = set(Note.objects.all())
        self.assertEqual(
            self.not_author_client.post(DELETE_NOTE_URL).status_code,
            HTTPStatus.NOT_FOUND
        )
        self.assertEqual(notes_before, set(Note.objects.all()))
        note_after_attempt = Note.objects.get(slug=self.note.slug)
        self.assertEqual(note_after_attempt.title, self.note.title)
        self.assertEqual(note_after_attempt.text, self.note.text)
        self.assertEqual(note_after_attempt.slug, self.note.slug)
        self.assertEqual(note_after_attempt.author, self.note.author)

    def test_not_author_cannot_edit_note(self):
        self.assertEqual(
            self.not_author_client.post(EDIT_NOTE_URL).status_code,
            HTTPStatus.NOT_FOUND
        )
        note_after_attempt = Note.objects.get(slug=self.note.slug)
        self.assertEqual(note_after_attempt.title, self.note.title)
        self.assertEqual(note_after_attempt.text, self.note.text)
        self.assertEqual(note_after_attempt.slug, self.note.slug)
        self.assertEqual(note_after_attempt.author, self.note.author)

    def test_author_can_edit_note(self):
        self.assertEqual(
            self.author_client.post(
                EDIT_NOTE_URL, data=self.note_data
            ).status_code,
            HTTPStatus.FOUND
        )
        updated_note = Note.objects.get(slug=self.note_data['slug'])
        self.assertEqual(updated_note.title, self.note_data['title'])
        self.assertEqual(updated_note.text, self.note_data['text'])
        self.assertEqual(updated_note.slug, self.note_data['slug'])
        self.assertEqual(updated_note.author, self.note.author)

    def test_author_can_delete_note(self):
        notes_before = set(Note.objects.all())
        self.assertEqual(
            self.author_client.post(DELETE_NOTE_URL).status_code,
            HTTPStatus.FOUND
        )
        notes_after = set(Note.objects.all())
        notes = notes_before - notes_after
        self.assertEqual(len(notes), 1)
        note = notes.pop()
        self.assertEqual(note.title, self.note.title)
        self.assertEqual(note.text, self.note.text)
        self.assertEqual(note.slug, self.note.slug)
        self.assertEqual(note.author, self.note.author)
