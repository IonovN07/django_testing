from http import HTTPStatus

import pytest
from news.forms import CommentForm
from yanews.settings import NEWS_COUNT_ON_HOME_PAGE as NEWS_PER_PAGE

HOME_URL = pytest.lazy_fixture('home_url')
DETAIL_URL = pytest.lazy_fixture('detail_url')

pytestmark = pytest.mark.django_db

# @pytest.mark.parametrize(
#     'url',
#     [
#         DETAIL_URL,
#     ],
# )
# def get_news_detail_url():
#     return url

@pytest.mark.parametrize(
    'url',
    [
        HOME_URL,
    ],
)
def test_news_count(client, sample_news, url):
    response = client.get(url)
    assert len(response.context['object_list']) == NEWS_PER_PAGE


# def test_comments_order_on_news_page(client, create_comments, news):
#     response = client.get(get_news_detail_url(news))
#     assert response.status_code == HTTPStatus.OK
#     news_comments = response.context['news'].comment_set.all()
#     timestamps = [comment.created for comment in news_comments]
#     assert timestamps == sorted(timestamps)


# def test_anonymous_client_has_no_form(client, news):
#     response = client.get(get_news_detail_url(news))
#     assert 'form' not in response.context


# def test_authorized_client_has_form(not_author_client, news):
#     response = not_author_client.get(get_news_detail_url(news))
#     assert 'form' in response.context
#     assert isinstance(response.context['form'], CommentForm)
