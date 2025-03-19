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
    REDIRECT_ADD_URL,
    REDIRECT_DELETE_URL,
    REDIRECT_DETAIL_URL,
    REDIRECT_EDIT_URL,
    REDIRECT_LIST_URL,
    REDIRECT_SUCCESS_URL,
    BaseTest
)


class TestRoutes(BaseTest):

    def test_response_codes(self):
        cases = [
            [HOME_URL, self.client, HTTPStatus.OK],
            [LOGIN_URL, self.client, HTTPStatus.OK],
            [LOGOUT_URL, self.client, HTTPStatus.OK],
            [SIGNUP_URL, self.client, HTTPStatus.OK],

            [SUCCESS_URL, self.not_author_client, HTTPStatus.OK],
            [LIST_URL, self.not_author_client, HTTPStatus.OK],
            [ADD_URL, self.not_author_client, HTTPStatus.OK],

            [EDIT_NOTE_URL, self.author_client, HTTPStatus.OK],
            [EDIT_NOTE_URL, self.not_author_client, HTTPStatus.NOT_FOUND],
            [DELETE_NOTE_URL, self.author_client, HTTPStatus.OK],
            [DELETE_NOTE_URL, self.not_author_client, HTTPStatus.NOT_FOUND],
            [DETAIL_NOTE_URL, self.author_client, HTTPStatus.OK],
            [DETAIL_NOTE_URL, self.not_author_client, HTTPStatus.NOT_FOUND],

            [EDIT_NOTE_URL, self.client, HTTPStatus.FOUND],
            [DELETE_NOTE_URL, self.client, HTTPStatus.FOUND],
            [DETAIL_NOTE_URL, self.client, HTTPStatus.FOUND],
            [ADD_URL, self.client, HTTPStatus.FOUND],
            [LIST_URL, self.client, HTTPStatus.FOUND],
            [SUCCESS_URL, self.client, HTTPStatus.FOUND]
        ]

        for url, client, expected_status in cases:
            with self.subTest(url=url, client=client):
                self.assertEqual(client.get(url).status_code, expected_status)

    def test_redirects_for_anonymous_client(self):
        cases = [
            (EDIT_NOTE_URL, REDIRECT_EDIT_URL),
            (DELETE_NOTE_URL, REDIRECT_DELETE_URL),
            (DETAIL_NOTE_URL, REDIRECT_DETAIL_URL),
            (ADD_URL, REDIRECT_ADD_URL),
            (LIST_URL, REDIRECT_LIST_URL),
            (SUCCESS_URL, REDIRECT_SUCCESS_URL),
        ]
        for url, redirect_url in cases:
            with self.subTest(url=url):
                self.assertRedirects(
                    self.client.get(url),
                    redirect_url
                )
