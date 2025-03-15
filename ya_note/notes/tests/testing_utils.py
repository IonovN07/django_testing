from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from pytils.translit import slugify

from notes.models import Note

User = get_user_model()


HOME_URL = reverse('notes:home')
LOGIN_URL = reverse('users:login')
LOGOUT_URL = reverse('users:logout')
SIGNUP_URL = reverse('users:signup')
SUCCESS_URL = reverse('notes:success')
LIST_URL = reverse('notes:list')
ADD_URL = reverse('notes:add')

NOTE_SLUG = 'note-slug'

EDIT_NOTE_URL = reverse('notes:edit', args=(NOTE_SLUG,))
DELETE_NOTE_URL = reverse('notes:delete', args=(NOTE_SLUG,))
DETAIL_NOTE_URL = reverse('notes:detail', args=(NOTE_SLUG,))


class BaseTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор')
        cls.not_author = User.objects.create(username='Не автор')
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст заметки',
            slug=NOTE_SLUG,
            author=cls.author
        )
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.not_author_client = Client()
        cls.not_author_client.force_login(cls.not_author)

        cls.note_data = {
            'title': 'Новый заголовок',
            'text': 'Новый текст',
            'slug': 'new-slug'
        }

    # @classmethod
    # def get_note_data(self):
    #     data = self.note_data.copy()
    #     data['slug'] = slugify(data['title'])
    #     return data