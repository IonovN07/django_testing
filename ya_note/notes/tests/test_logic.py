from http import HTTPStatus

from django.urls import reverse
from pytils.translit import slugify

from notes.models import Note
from notes.forms import WARNING
from .testing_utils import (
    ADD_URL,
    DELETE_NOTE_URL,
    DETAIL_NOTE_URL,
    EDIT_NOTE_URL,
    HOME_URL,
    LIST_URL,
    LOGIN_URL,
    LOGOUT_URL,
    SIGNUP_URL,
    SUCCESS_URL,
    BaseTest
)


class TestLogic(BaseTest):

    def test_not_unique_slug(self):
        note_duplicate_slug = self.note_data.copy()
        note_duplicate_slug['slug'] = self.note.slug
        self.assertFormError(
            self.author_client.post(
            ADD_URL,
            data=note_duplicate_slug
        ),
            'form',
            'slug',
            errors=(self.note.slug + WARNING)
        )
        self.assertEqual(Note.objects.count(), 1)

    # def test_not_unique_slug(self):
    #     self.author_client
    #     self.assertFormError(
    #         self.client.post(reverse('notes:add'), data=self.note_data),
    #         'form',
    #         'slug',
    #         errors=(
    #             f'{self.note_data.slug} - такой slug уже существует, '
    #             'придумайте уникальное значение!'
    #         )
    #     )

    # def test_slug_automatic_generation(self):
    #     self.assertEqual(
    #         self.note_author.slug,
    #         slugify(self.note_author.title)
    #     )

    # def test_note_creation_with_author(self):
    #     self.client.force_login(self.reader)
    #     self.client.post(reverse('notes:add'), NOTE_DATA)
    #     self.assertEqual(Note.objects.count(), 3)
    #     new_note = Note.objects.get(title='Новая заметка')
    #     self.assertEqual(new_note.author, self.reader)

    # def test_anonymous_user_cant_create_note(self):
    #     self.client.post(reverse('notes:add'), NOTE_DATA)
    #     self.assertEqual(Note.objects.count(), 2)

    # def test_user_permissions_for_editing_and_deleting_notes(self):
    #     test_cases = (
    #         (self.reader, 'delete', HTTPStatus.NOT_FOUND),
    #         (self.reader, 'edit', HTTPStatus.NOT_FOUND),
    #         (self.author, 'edit', HTTPStatus.OK),
    #         (self.author, 'delete', HTTPStatus.FOUND),
    #     )
    #     for user, action, expected_status in test_cases:
    #         with self.subTest(user=user, action=action):
    #             self.client.force_login(user)

    #             if action == 'delete':
    #                 url = reverse(
    #                     'notes:delete',
    #                     args=(self.note_author.slug,)
    #                 )
    #             elif action == 'edit':
    #                 url = reverse('notes:edit', args=(self.note_author.slug,))

    #             self.assertEqual(
    #                 self.client.post(url).status_code,
    #                 expected_status
    #             )
