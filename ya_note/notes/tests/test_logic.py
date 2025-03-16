from http import HTTPStatus

from pytils.translit import slugify

from notes.models import Note
from notes.forms import WARNING
from .testing_utils import (
    ADD_URL,
    DELETE_NOTE_URL,
    EDIT_NOTE_URL,
    BaseTest
)


class TestLogic(BaseTest):

    def test_not_unique_slug(self):
        note_duplicate_slug = self.note_data.copy()
        note_duplicate_slug['slug'] = self.note.slug
        self.assertFormError(
            self.author_client.post(ADD_URL, data=note_duplicate_slug),
            'form',
            'slug',
            errors=(self.note.slug + WARNING)
        )
        self.assertEqual(Note.objects.count(), 1)

    def test_slug_is_auto_generated_when_not_provided(self):
        note_data_not_slug = self.note_data.copy()
        note_data_not_slug.pop('slug', None)
        existing_notes = set(Note.objects.all())
        self.assertEqual(
            self.author_client.post(
                ADD_URL, data=note_data_not_slug
            ).status_code,
            302
        )
        new_notes = set(Note.objects.all())
        created_notes = new_notes - existing_notes
        self.assertEqual(len(created_notes), 1)
        new_note = created_notes.pop()
        expected_slug = slugify(self.note_data['title'])
        self.assertEqual(new_note.slug, expected_slug)
        self.assertEqual(new_note.title, self.note_data['title'])
        self.assertEqual(new_note.text, self.note_data['text'])
        self.assertEqual(new_note.author, self.author)

    def test_note_creation_with_author(self):
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

    def test_note_creation_without_authorization(self):
        initial_note_count = Note.objects.count()
        self.assertIn(
            self.client.post(ADD_URL, self.note_data).status_code,
            [302, 403]
        )
        self.assertEqual(Note.objects.count(), initial_note_count)

    def test_reader_cannot_delete_note(self):
        self.assertEqual(
            self.not_author_client.post(DELETE_NOTE_URL).status_code,
            HTTPStatus.NOT_FOUND
        )

    def test_reader_cannot_edit_note(self):
        self.assertEqual(
            self.not_author_client.post(EDIT_NOTE_URL).status_code,
            HTTPStatus.NOT_FOUND
        )

    def test_author_can_edit_note(self):
        self.author_client
        url = EDIT_NOTE_URL
        response = self.author_client.post(url, data=self.note_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, self.note_data['title'])
        self.assertEqual(self.note.text, self.note_data['text'])
        self.assertEqual(self.note.slug, self.note_data['slug'])
        self.assertEqual(self.note.author, self.author)

    def test_author_can_delete_note(self):
        self.assertEqual(
            self.author_client.post(DELETE_NOTE_URL).status_code,
            HTTPStatus.FOUND
        )
