from .testing_utils import (
    ADD_URL,
    EDIT_NOTE_URL,
    LIST_URL,
    BaseTest
)

from notes.forms import NoteForm


class TestFormPage(BaseTest):

    def test_notes_list_for_author(self):
        self.assertIn(
            self.note,
            self.author_client.get(LIST_URL).context['object_list']
        )
        note = (
            self.author_client.get(LIST_URL)
            .context['object_list']
            .filter(pk=self.note.id)
            .first()
        )
        self.assertIsNotNone(note, "Заметка не найдена в контексте")
        self.assertEqual(note.title, self.note.title)
        self.assertEqual(note.text, self.note.text)
        self.assertEqual(note.slug, self.note.slug)
        self.assertEqual(note.author, self.note.author)

    def test_notes_list_for_not_author(self):
        self.assertNotIn(
            self.note,
            self.not_author_client.get(LIST_URL).context['object_list']
        )

    def test_pages_contains_form(self):
        self.author_client
        form_urls = (ADD_URL, EDIT_NOTE_URL)
        for url in form_urls:
            with self.subTest(url):
                self.assertIn('form', self.author_client.get(url).context)
                self.assertIsInstance(
                    self.author_client.get(url).context.get('form'),
                    NoteForm
                )
