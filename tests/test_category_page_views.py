from http import HTTPStatus

import pytest

pytestmark = [
    pytest.mark.django_db,
]


def test_category_page(
        user_client, posts_with_published_locations,
        category_page_post_list_context_key):
    category = posts_with_published_locations[0].category

    def get_category_posts():
        response = user_client.get(f'/category/{category.slug}/')
        return response.context.get(category_page_post_list_context_key)

    context_post_list = get_category_posts()
    assert len(context_post_list) == len(
        posts_with_published_locations), (
        'Убедитесь, что при обращении к странице `/category/<slug:slug>/` в '
        'словаре контекста под ключом '
        f'`{category_page_post_list_context_key}` '
        'передаются все не снятые с публикации записи, принадлежащие этой '
        'категории.'
    )
    context_post_list[0].is_published = False
    context_post_list[0].save()
    assert all(x.is_published for x in get_category_posts()), (
        'Проверьте, что при обращении к странице `/category/<slug:slug>/` '
        'в словаре контекста '
        f'под ключом `{category_page_post_list_context_key}`, '
        'передаются только опубликованные записи.'
    )


@pytest.mark.parametrize('key', [
    'title',
    ('category', 'title'),
    ('category', 'slug'),
    ('location', 'name')
])
def test_category_page_check_context_keys(
        key, user_client, posts_with_published_locations,
        published_category, category_page_post_list_context_key
):
    response = user_client.get(f'/category/{published_category.slug}/')
    context_post_list = response.context.get(
        category_page_post_list_context_key)
    html = response.content.decode('utf-8')
    if isinstance(key, tuple):
        key_1, key_2 = key
        assert getattr(
            getattr(context_post_list[0], key_1), key_2) in html, (
            'На странице категории '
            f'не использовано значение атрибута `{key_1}.{key_2}`.'
        )
    else:
        assert getattr(context_post_list[0], key) in html, (
            'На странице категории '
            f'не использовано значение атрибута публикаций `{key}`.'
        )


def test_category_page_category_unpublished(
        user_client, posts_with_unpublished_category,
        category_page_post_list_context_key
):
    category_slug = posts_with_unpublished_category[0].category.slug
    response = user_client.get(f'/category/{category_slug}/')
    assert response.status_code == HTTPStatus.NOT_FOUND, (
        'Убедитесь, что страница категории, снятой с публикации, '
        'возвращает статус 404.'
    )


def test_category_page_posts_unpublished(
        user_client, unpublished_posts_with_published_locations,
        category_page_post_list_context_key
):
    category_slug = unpublished_posts_with_published_locations[0].category.slug
    response = user_client.get(f'/category/{category_slug}/')
    if response.status_code == HTTPStatus.OK:
        context_post_list = response.context.get(
            category_page_post_list_context_key)
        assert len(context_post_list) == 0, (
            'Убедитесь, что когда в категории нет опубликованных постов, '
            'они не передаются в контекст её страницы.'
        )


def test_category_page_pub_date_later_today(
        user_client,
        posts_with_future_date,
        category_page_post_list_context_key
):
    if not posts_with_future_date[0].category:
        raise AssertionError(
            'В модели `Post` в атрибуте `category` '
            'проверьте значение параметра `blank` на соответствие заданию.')
    category_slug = posts_with_future_date[0].category.slug
    response = user_client.get(f'/category/{category_slug}/')
    if response.status_code == HTTPStatus.OK:
        context_post_list = response.context.get(
            category_page_post_list_context_key)
        assert len(context_post_list) == 0, (
            'Убедитесь, что на странице категории '
            'не выводятся записи с датой публикации в будущем.'
        )


def test_category_page_posts_with_location(
        user_client, posts_with_published_locations,
        category_page_post_list_context_key
):
    category = posts_with_published_locations[0].category
    response = user_client.get(f'/category/{category.slug}/')
    context_post_list = response.context.get(
        category_page_post_list_context_key)
    assert all(x.location for x in context_post_list), (
        'Убедитесь, что на странице категории '
        'в объектах постов, отмеченных опубликованной географической '
        'меткой, передаётся ключ `location` и его значение.'
    )


def test_category_page_posts_with_unpublished_locations(
        user_client,
        posts_with_unpublished_locations, category_page_post_list_context_key
):
    category = posts_with_unpublished_locations[0].category
    response = user_client.get(f'/category/{category.slug}/')
    context_post_list = response.context.get(
        category_page_post_list_context_key)
    assert len(context_post_list) == len(posts_with_unpublished_locations), (
        ' Убедитесь, что в словарь контекста страницы категории '
        'попадают и те записи этой категории, '
        'географическая метка которых снята с публикации.'
    )


def test_many_posts_on_category_page(
        user_client, many_posts_with_published_locations,
        category_page_post_list_context_key):
    category = many_posts_with_published_locations[0].category
    response = user_client.get(f'/category/{category.slug}/')
    context_post_list = response.context.get(
        category_page_post_list_context_key)
    assert len(context_post_list) == len(
        many_posts_with_published_locations), (
        'Убедитесь, что на странице категории '
        'отображаются все относящиеся к ней опубликованные посты.'
    )


def test_no_other_posts_on_category_page(
        user_client, posts_with_published_locations,
        posts_with_unpublished_category,
        posts_with_published_locations_from_another_published_category,
        category_page_post_list_context_key):
    category = posts_with_published_locations[0].category
    response = user_client.get(f'/category/{category.slug}/')
    context_post_list = response.context.get(
        category_page_post_list_context_key)
    assert len(context_post_list) == len(
        posts_with_published_locations), (
        'Убедитесь, что на странице категории '
        'отображаются опубликованные посты, относящиеся исключительно к этой '
        'категории.'
    )
