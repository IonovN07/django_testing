import pytest

from news.forms import CommentForm
from yanews.settings import NEWS_COUNT_ON_HOME_PAGE as NEWS_PER_PAGE


pytestmark = pytest.mark.django_db


def test_news_count(client, sample_news, home_url):
    assert len(client.get(home_url).context['object_list']) == NEWS_PER_PAGE


def test_comments_order_on_news_page(client, sample_comments, detail_url):
    timestamps = [
        comment.created
        for comment in client.get(detail_url).context['news'].comment_set.all()
    ]
    assert timestamps == sorted(timestamps)


def test_anonymous_client_has_no_form(client, detail_url):
    assert 'form' not in client.get(detail_url).context


def test_authorized_client_has_form(not_author_client, detail_url):
    assert isinstance(
        not_author_client.get(detail_url).context.get('form'),
        CommentForm
    )
