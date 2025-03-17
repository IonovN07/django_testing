from http import HTTPStatus

import pytest
from pytest_django.asserts import assertRedirects

HOME_URL = pytest.lazy_fixture('home_url')
DETAIL_URL = pytest.lazy_fixture('detail_url')
LOGIN_URL = pytest.lazy_fixture('login_url')
LOGOUT_URL = pytest.lazy_fixture('logout_url')
SIGNUP_URL = pytest.lazy_fixture('signup_url')
EDIT_URL = pytest.lazy_fixture('edit_url')
DELETE_URL = pytest.lazy_fixture('delete_url')

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'url, client_fixture, expected_status',
    [
        (HOME_URL, 'client', HTTPStatus.OK),
        (DETAIL_URL, 'client', HTTPStatus.OK),
        (LOGIN_URL, 'client', HTTPStatus.OK),
        (LOGOUT_URL, 'client', HTTPStatus.OK),
        (SIGNUP_URL, 'client', HTTPStatus.OK),
        (EDIT_URL, 'not_author_client', HTTPStatus.NOT_FOUND),
        (EDIT_URL, 'author_client', HTTPStatus.OK),
        (DELETE_URL, 'not_author_client', HTTPStatus.NOT_FOUND),
        (DELETE_URL, 'author_client', HTTPStatus.OK),
    ],
)
def test_pages_availability(url, client_fixture, expected_status, request):
    assert request.getfixturevalue(
        client_fixture
    ).get(url).status_code == expected_status


@pytest.mark.parametrize(
    'url, expected_login_url',
    [
        (EDIT_URL, LOGIN_URL),
        (DELETE_URL, LOGIN_URL),
    ],
)
def test_redirect_for_anonymous_client(client, url, expected_login_url):
    assertRedirects(client.get(url), f'{expected_login_url}?next={url}')
