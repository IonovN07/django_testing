from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

DETAIL_URL = pytest.lazy_fixture('detail_url')
DELETE_URL = pytest.lazy_fixture('delete_url')
EDIT_URL = pytest.lazy_fixture('edit_url')

COMMENT_DATA = {
    'text': 'Новый текст'
}

pytestmark = pytest.mark.django_db


def parametrize_with_detail_url(test_func):
    return pytest.mark.parametrize('url', [DETAIL_URL])(test_func)


def parametrize_with_delete_url(test_func):
    return pytest.mark.parametrize('url_delete', [DELETE_URL])(test_func)


def parametrize_with_edit_url(test_func):
    return pytest.mark.parametrize('url_edit', [EDIT_URL])(test_func)


@parametrize_with_detail_url
def test_anonymous_user_cant_create_comment(client, url):
    initial_comments = list(Comment.objects.all())
    client.post(url, data=COMMENT_DATA)
    final_comments = list(Comment.objects.all())
    assert initial_comments == final_comments


@parametrize_with_detail_url
def test_user_can_create_comment(not_author, not_author_client, news, url):
    existing_comments = set(Comment.objects.all())
    not_author_client.post(
        url,
        data=COMMENT_DATA
    )
    new_comments = set(Comment.objects.all())
    created_comments = new_comments - existing_comments
    assert (len(created_comments) == 1)
    new_comment = created_comments.pop()
    assert new_comment.text == COMMENT_DATA['text']
    assert new_comment.news == news
    assert new_comment.author == not_author


@parametrize_with_detail_url
@pytest.mark.parametrize('bad_word', BAD_WORDS)
def test_user_cant_use_bad_words(author_client, url, bad_word):
    data = {**COMMENT_DATA}
    data['text'] = f'Текст, {bad_word}, еще текст'
    form = author_client.post(
        url,
        data=data
    ).context['form']
    assert 'text' in form.errors
    assert WARNING in form.errors['text']
    assert Comment.objects.count() == 0


@parametrize_with_detail_url
@parametrize_with_delete_url
def test_author_can_delete_comment(author_client, comment, url, url_delete):
    assertRedirects(author_client.post(url_delete), url + '#comments')
    assert Comment.objects.count() == 0


@parametrize_with_delete_url
def test_user_cant_delete_comment_of_another_user(
    not_author_client, comment, url_delete
):
    original_comment = Comment.objects.get(pk=comment.pk)
    assert (
        not_author_client.post(url_delete).status_code == HTTPStatus.NOT_FOUND)
    assert Comment.objects.count() == 1
    current_comment = Comment.objects.get(pk=comment.pk)
    assert original_comment.text == current_comment.text
    assert original_comment.news == current_comment.news
    assert original_comment.author == current_comment.author


@parametrize_with_detail_url
@parametrize_with_edit_url
def test_author_can_edit_comment(
    author, author_client, news, comment, url, url_edit
):
    assertRedirects(
        author_client.post(
            url_edit,
            data=COMMENT_DATA
        ), url + '#comments'
    )
    assert (
        author_client.get(url_edit).context.get('form').initial['text']
        == COMMENT_DATA['text']
    )
    updated_comment = Comment.objects.get(pk=comment.pk)
    assert updated_comment.text == COMMENT_DATA['text']
    assert updated_comment.news == news
    assert updated_comment.author == author


@parametrize_with_edit_url
def test_user_cant_edit_comment_of_another_user(
    not_author_client, comment, url_edit
):
    original_comment = Comment.objects.get(pk=comment.pk)
    assert (
        not_author_client.post(
            url_edit,
            data=COMMENT_DATA
        ).status_code == HTTPStatus.NOT_FOUND
    )
    current_comment = Comment.objects.get(pk=comment.pk)
    assert original_comment.text == current_comment.text
    assert original_comment.author == current_comment.author
    assert original_comment.news == current_comment.news
