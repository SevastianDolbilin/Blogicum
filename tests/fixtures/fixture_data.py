from datetime import datetime, timedelta

import pytest
import pytz
from django.contrib.auth import get_user_model

N_TEST_POSTS = 4
N_POSTS_LIMIT = 5


@pytest.fixture
def published_locations(mixer):
    return mixer.cycle(N_TEST_POSTS).blend('blog.Location')


@pytest.fixture
def unpublished_locations(mixer):
    return mixer.cycle(N_TEST_POSTS).blend('blog.Location', is_published=False)


@pytest.fixture
def posts_with_unpublished_category(mixer):
    return mixer.cycle(N_TEST_POSTS).blend(
        'blog.Post', category__is_published=False)


@pytest.fixture
def posts_with_future_date(mixer):
    date_later_now = (
        datetime.now(tz=pytz.UTC) + timedelta(days=date)
        for date in range(1, 11)
    )
    return mixer.cycle(N_TEST_POSTS).blend(
        'blog.Post', pub_date=date_later_now)


@pytest.fixture
def posts_with_published_locations(
        mixer, published_locations, published_category):
    return mixer.cycle(N_TEST_POSTS).blend(
        'blog.Post', category=published_category,
        location=mixer.sequence(*published_locations))


@pytest.fixture
def unpublished_posts_with_published_locations(
        mixer, published_locations, published_category):
    return mixer.cycle(N_TEST_POSTS).blend(
        'blog.Post', is_published=False, category=published_category,
        location=mixer.sequence(*published_locations))


@pytest.fixture
def posts_with_published_locations_from_another_published_category(
        mixer, published_locations, another_published_category):
    return mixer.cycle(N_TEST_POSTS).blend(
        'blog.Post', category=another_published_category,
        location=mixer.sequence(*published_locations))


@pytest.fixture
def posts_with_unpublished_locations(
        mixer, published_category, unpublished_locations):
    return mixer.cycle(N_TEST_POSTS).blend(
        'blog.Post', location=mixer.sequence(*unpublished_locations),
        category=published_category)


@pytest.fixture
def published_category(mixer):
    return mixer.blend('blog.Category', is_published=True)


@pytest.fixture
def another_published_category(mixer):
    return mixer.blend('blog.Category', is_published=True)


@pytest.fixture
def published_location(mixer):
    return mixer.blend('blog.Location', is_published=True)


@pytest.fixture
def unpublished_location(mixer):
    return mixer.blend('blog.Location', is_published=False)


@pytest.fixture
def unpublished_post(mixer):
    return mixer.blend('blog.Post', is_published=False)


@pytest.fixture
def unpublished_category(mixer):
    return mixer.blend('blog.Category', is_published=False)


@pytest.fixture
def post_with_unpublished_category(mixer, unpublished_category):
    return mixer.blend('blog.Post', category=unpublished_category)


@pytest.fixture
def post_with_published_location(
        mixer, published_location, published_category):
    return mixer.blend('blog.Post', location=published_location,
                       category=published_category)


@pytest.fixture
def post_with_unpublished_location(
        mixer, unpublished_location, published_category):
    return mixer.blend(
        'blog.Post', category=published_category,
        location=unpublished_location)


@pytest.fixture
def post_with_future_date(mixer):
    date_later_now = datetime.now(tz=pytz.UTC) + timedelta(days=1)
    return mixer.blend('blog.Post', pub_date=date_later_now)


@pytest.fixture
def author(mixer):
    User = get_user_model()
    return mixer.blend(User)


@pytest.fixture
def many_posts_with_published_locations(
        mixer, published_locations, published_category):
    return mixer.cycle(N_POSTS_LIMIT * 2).blend(
        'blog.Post', category=published_category,
        location=mixer.sequence(*published_locations))


@pytest.fixture
def posts_with_author(mixer, author):
    return mixer.cycle(2).blend('blog.Post', author=author)
