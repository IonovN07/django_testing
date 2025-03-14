from http import HTTPStatus

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


class TestRoutes(BaseTest):

    def test_response_codes(self):
        cases = [
            [HOME_URL, None, HTTPStatus.OK],
            [LOGIN_URL, None, HTTPStatus.OK],
            [LOGOUT_URL, None, HTTPStatus.OK],
            [SIGNUP_URL, None, HTTPStatus.OK],

            [SUCCESS_URL, self.not_author_client, HTTPStatus.OK],
            [LIST_URL, self.not_author_client, HTTPStatus.OK],
            [ADD_URL, self.not_author_client, HTTPStatus.OK],

            [EDIT_NOTE_URL, self.author_client, HTTPStatus.OK],
            [EDIT_NOTE_URL, self.not_author_client, HTTPStatus.NOT_FOUND],
            [DELETE_NOTE_URL, self.author_client, HTTPStatus.OK],
            [DELETE_NOTE_URL, self.not_author_client, HTTPStatus.NOT_FOUND],
            [DETAIL_NOTE_URL, self.author_client, HTTPStatus.OK],
            [DETAIL_NOTE_URL, self.not_author_client, HTTPStatus.NOT_FOUND],
        ]

        for url, client, expected_status in cases:
            client = self.client if client is None else client
            with self.subTest(url=url, client=client):
                self.assertEqual(client.get(url).status_code, expected_status)

    def test_redirects_for_anonymous_client(self):
        cases = [
            EDIT_NOTE_URL,
            DELETE_NOTE_URL,
            DETAIL_NOTE_URL,
            ADD_URL,
            LIST_URL,
            SUCCESS_URL,
        ]
        for url in cases:
            with self.subTest(url=url):
                self.assertRedirects(
                    self.client.get(url),
                    f'{LOGIN_URL}?next={url}'
                )
