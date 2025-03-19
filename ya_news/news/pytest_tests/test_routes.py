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
REDIRECT_DELETE_URL = pytest.lazy_fixture('login_redirect_delete_url')
RREDIRECT_EDIT_URL = pytest.lazy_fixture('login_redirect_edit_url')
ANONYMOUS_CLIENT = pytest.lazy_fixture('anonymous_client')
AUTHOR_CLIENT = pytest.lazy_fixture('author_client')
NOT_AUTHOR_CLIENT = pytest.lazy_fixture('not_author_client')

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'url, client, expected_status',
    [
        (HOME_URL, ANONYMOUS_CLIENT, HTTPStatus.OK),
        (DETAIL_URL, ANONYMOUS_CLIENT, HTTPStatus.OK),
        (LOGIN_URL, ANONYMOUS_CLIENT, HTTPStatus.OK),
        (LOGOUT_URL, ANONYMOUS_CLIENT, HTTPStatus.OK),
        (SIGNUP_URL, ANONYMOUS_CLIENT, HTTPStatus.OK),
        (EDIT_URL, NOT_AUTHOR_CLIENT, HTTPStatus.NOT_FOUND),
        (EDIT_URL, AUTHOR_CLIENT, HTTPStatus.OK),
        (DELETE_URL, NOT_AUTHOR_CLIENT, HTTPStatus.NOT_FOUND),
        (DELETE_URL, AUTHOR_CLIENT, HTTPStatus.OK),
        (EDIT_URL, ANONYMOUS_CLIENT, HTTPStatus.FOUND),
        (DELETE_URL, ANONYMOUS_CLIENT, HTTPStatus.FOUND),
    ],
)
def test_pages_availability(url, client, expected_status):
    assert client.get(url).status_code == expected_status


@pytest.mark.parametrize(
    'url, expected_login_url',
    [
        (EDIT_URL, RREDIRECT_EDIT_URL),
        (DELETE_URL, REDIRECT_DELETE_URL),
    ],
)
def test_redirect_for_anonymous_client(client, url, expected_login_url):
    assertRedirects(client.get(url), expected_login_url)
