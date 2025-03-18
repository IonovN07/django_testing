import pytest

from news.forms import CommentForm
from yanews.settings import NEWS_COUNT_ON_HOME_PAGE as NEWS_PER_PAGE

HOME_URL = pytest.lazy_fixture('home_url')
DETAIL_URL = pytest.lazy_fixture('detail_url')

pytestmark = pytest.mark.django_db


def parametrize_with_detail_url(test_func):
    return pytest.mark.parametrize('url', [DETAIL_URL])(test_func)


@pytest.mark.parametrize(
    'url',
    [
        HOME_URL,
    ],
)
def test_news_count(client, sample_news, url):
    assert len(client.get(url).context['object_list']) == NEWS_PER_PAGE


@parametrize_with_detail_url
def test_comments_order_on_news_page(client, sample_comments, url):
    timestamps = [
        comment.created
        for comment in client.get(url).context['news'].comment_set.all()
    ]
    assert timestamps == sorted(timestamps)


@parametrize_with_detail_url
def test_anonymous_client_has_no_form(client, url):
    assert 'form' not in client.get(url).context


@parametrize_with_detail_url
def test_authorized_client_has_form(not_author_client, url):
    assert (
        not_author_client.get(url).context.get('form') is not None
        and isinstance(
            not_author_client.get(url).context.get('form'),
            CommentForm
        )
    )
