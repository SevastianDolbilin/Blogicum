import pytest

from tests.fixtures.fixture_data import N_TEST_POSTS, N_POSTS_LIMIT

pytestmark = [
    pytest.mark.django_db,
]


def test_all_unpublished(
        user_client, unpublished_posts_with_published_locations,
        main_page_post_list_context_key):
    response = user_client.get('/')
    context_post_list = response.context.get(main_page_post_list_context_key)
    assert len(context_post_list) == 0, (
        'Убедитесь, что если в проекте нет ни одного опубликованного поста - '
        'то на главной странице нет записей.'
    )


def test_mixed_published(
        user_client, posts_with_published_locations,
        unpublished_posts_with_published_locations,
        main_page_post_list_context_key
):
    response = user_client.get('/')
    context_post_list = response.context.get(main_page_post_list_context_key)
    n_expected = len(posts_with_published_locations)
    assert len(context_post_list) == n_expected, (
        'Убедитесь, что при обращении к главной странице в словарь контекста '
        f'под ключом `{main_page_post_list_context_key}` передаются только '
        'опубликованные записи с опубликованной категорией '
        'и датой публикации в прошлом.'
    )
    assert all(x.is_published for x in context_post_list), (
        'При обращении к главной странице в словаре контекста '
        f'под ключом `{main_page_post_list_context_key}` '
        'должны передаваться только опубликованные записи.'
    )


@pytest.mark.parametrize('key', [
    'title',
    ('category', 'title'),
    ('category', 'slug'),
    ('location', 'name')
])
def test_check_context_keys(
        key,
        user_client,
        posts_with_published_locations, main_page_post_list_context_key):
    response = user_client.get('/')
    context_post_list = response.context.get(main_page_post_list_context_key)
    html = response.content.decode('utf-8')
    if isinstance(key, tuple):
        key_1, key_2 = key
        assert getattr(getattr(context_post_list[0], key_1), key_2) in html, (
            'На главной странице '
            f'не использовано значение атрибута `{key_1}.{key_2}`.'
        )
    else:
        assert getattr(context_post_list[0], key) in html, (
            'На главной странице '
            f'не использовано значение атрибута публикаций `{key}`.'
        )


def test_category_unpublished(
        user_client, posts_with_unpublished_category,
        main_page_post_list_context_key):
    response = user_client.get('/')
    context_post_list = response.context.get(main_page_post_list_context_key)
    assert len(context_post_list) == 0, (
        'Если категория снята с публикации, '
        'то на главной странице не должны отображаться '
        'относящиеся к ней посты.'
    )


def test_pub_date_later_today(
        user_client, posts_with_future_date, main_page_post_list_context_key):
    response = user_client.get('/')
    context_post_list = response.context.get(main_page_post_list_context_key)
    assert len(context_post_list) == 0, (
        'Если дата публикации поста позже текущего времени, '
        'он не должен отображаться на главной странице.'
    )


def test_posts_with_published_location(
        user_client, posts_with_published_locations,
        main_page_post_list_context_key
):
    response = user_client.get('/')
    context_post_list = response.context.get(main_page_post_list_context_key)
    assert all(x.location for x in context_post_list), (
        'Убедитесь, что в словаре контекста для главной страницы '
        'в объектах постов, '
        'отмеченных географической меткой, '
        'передаётся ключ `location` и значение этого ключа.'
    )


def test_posts_with_unpublished_locations(
        user_client,
        posts_with_unpublished_locations, main_page_post_list_context_key):
    response = user_client.get('/')
    context_post_list = response.context.get(main_page_post_list_context_key)
    assert len(context_post_list) == N_TEST_POSTS, (
        ' Убедитесь, что в словарь контекста главной страницы '
        'попадают даже те записи, '
        'географическая метка которых не опубликована.'
    )


def test_many_posts_on_main_page(
        user_client, many_posts_with_published_locations,
        main_page_post_list_context_key):
    response = user_client.get('/')
    context_post_list = response.context.get(main_page_post_list_context_key)
    assert len(context_post_list) == N_POSTS_LIMIT, (
        'Убедитесь, что на главной странице '
        f'отображается только {N_POSTS_LIMIT} последних публикаций.'
    )
