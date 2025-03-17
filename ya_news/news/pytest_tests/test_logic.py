import random
from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

DETAIL_URL = pytest.lazy_fixture('detail_url')

pytestmark = pytest.mark.django_db

def parametrize_with_detail_url(test_func):
    return pytest.mark.parametrize('url', [DETAIL_URL])(test_func)

@parametrize_with_detail_url
def test_anonymous_user_cant_create_comment(client, url):
    initial_comments = list(Comment.objects.all())
    data = {
        'title': 'Новый заголовок',
        'text': 'Новый текст'
    }
    client.post(url, data=data)
    final_comments = list(Comment.objects.all())
    assert initial_comments == final_comments

@parametrize_with_detail_url
def test_user_can_create_comment(not_author, not_author_client, news, url):
    existing_comments = set(Comment.objects.all())
    data = {
        'title': 'Новый заголовок',
        'text': 'Новый текст'
    }
    not_author_client.post(
        url,
        data=data
    )
    new_comments = set(Comment.objects.all())
    created_comments = new_comments - existing_comments 
    assert (len(created_comments) == 1)
    new_comment = created_comments.pop()
    assert new_comment.text == data['text']
    assert new_comment.news == news
    assert new_comment.author == not_author


# def test_user_cant_use_bad_words(author_client, news):
#     form = author_client.post(
#         get_news_detail_url(news),
#         data={'text': f'Текст, {random.choice(BAD_WORDS)}, еще текст'}
#     ).context['form']
#     assert 'text' in form.errors
#     assert WARNING in form.errors['text']
#     assert get_comment_count() == 0


# def test_author_can_delete_comment(author_client, comment, news):
#     response = author_client.post(reverse('news:delete', args=(comment.id,)))
#     assertRedirects(response, get_news_detail_url(news) + '#comments')
#     assert get_comment_count() == 0


# def test_user_cant_delete_comment_of_another_user(not_author_client, comment):
#     response = not_author_client.post(
#         reverse('news:delete', args=(comment.id,))
#     )
#     assert response.status_code == HTTPStatus.NOT_FOUND
#     assert get_comment_count() == 1


# def test_author_can_edit_comment(author_client, comment, news, comment_data):
#     comment_data['text'] = NEW_COMMENT_TEXT
#     assertRedirects(
#         author_client.post(
#             reverse('news:edit', args=(comment.id,)),
#             data=comment_data
#         ),
#         get_news_detail_url(news) + '#comments'
#     )
#     comment.refresh_from_db()
#     assert comment.text == NEW_COMMENT_TEXT


# def test_user_cant_edit_comment_of_another_user(
#     not_author_client, comment, news, comment_data
# ):
#     comment_data['text'] = NEW_COMMENT_TEXT
#     response = not_author_client.post(
#         reverse('news:edit', args=(comment.id,)),
#         data=comment_data
#     )
#     assert response.status_code == HTTPStatus.NOT_FOUND
#     comment.refresh_from_db()
#     assert comment.text != NEW_COMMENT_TEXT
