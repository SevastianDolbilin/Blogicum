from http import HTTPStatus

import pytest

from blog.models import Post

pytestmark = [
    pytest.mark.django_db,
]


def test_posts_page_pk_published_location(
        user_client, post_with_published_location, post_context_key):
    response = user_client.get(f'/posts/{post_with_published_location.id}/')
    assert response.status_code == HTTPStatus.OK, (
        'Убедитесь, что опубликованный пост с опубликованной категорией '
        'и датой публикации в прошлом отображается на отдельной странице '
        'поста.'
    )
    context_post = response.context.get(post_context_key)
    assert context_post == post_with_published_location, (
        'Убедитесь, что в контекст страницы `/posts/<int:pk>/` '
        f'под ключом `{post_context_key}` '
        'передаётся пост c идентификатором `pk`, '
        'где `pk` - параметр из строки GET-запроса.'
    )


def test_posts_page_pk_unpublished_location(
        user_client, post_with_unpublished_location, post_context_key):
    response = user_client.get(f'/posts/{post_with_unpublished_location.id}/')
    assert response.status_code == HTTPStatus.OK, (
        'Убедитесь, что опубликованный пост с опубликованной категорией '
        'и датой публикации в прошлом отображается на отдельной странице '
        'поста, даже если его локация снята с публикации.'
    )


def test_posts_page_pk_post_doesnt_exists(user_client):
    try:
        response = user_client.get('/posts/1/')
    except Post.DoesNotExist:
        raise AssertionError(
            'Убедитесь, что при обращении к странице несуществующего поста '
            'во view-функции не возникает необрабатываемого исключения.'
        )
    assert response.status_code != HTTPStatus.OK, (
        'Убедитесь, что при запросе к несуществующему посту не возвращается '
        'страница отдельного поста.'
    )


@pytest.mark.parametrize('key', [
    'title',
    'text',
    ('category', 'title'),
    ('category', 'slug'),
    ('location', 'name')
])
def test_posts_page_pk_check_context_keys(
        key, user_client, post_with_published_location,
        post_context_key
):
    response = user_client.get(
        f'/posts/{post_with_published_location.id}/')
    assert response.status_code == HTTPStatus.OK, (
        'Убедитесь, что страница отдельного поста существует и отображается '
        'в соответствии с заданием, если пост опубликован, '
        'у него указана географическая метка и опубликована категория.'
    )
    context_post = response.context.get(post_context_key)
    html = response.content.decode('utf-8')
    if isinstance(key, tuple):
        key_1, key_2 = key
        assert getattr(getattr(context_post, key_1), key_2) in html, (
            'На странице публикации '
            f'не использовано значение атрибута `{key_1}.{key_2}`.'
        )
    else:
        attr_val = getattr(context_post, key)
        if key == 'text':
            if attr_val in html:
                return
            else:
                attr_val = attr_val.replace('\n', '<br>')
        assert attr_val in html, (
            'На странице публикации '
            f'не использовано значение атрибута `{key}`.'
        )


def test_posts_page_pk_unpublished_post(user_client, unpublished_post):
    response = user_client.get(f'/posts/{unpublished_post.id}/')
    assert response.status_code == HTTPStatus.NOT_FOUND, (
        'Убедитесь, что страница поста, снятого с публикации, '
        'возвращает статус 404.'
    )


def test_posts_page_pk_pub_date_later_today(
        user_client, post_with_future_date):
    response = user_client.get(f'/posts/{post_with_future_date.id}/')
    assert response.status_code == HTTPStatus.NOT_FOUND, (
        'Убедитесь, что если для поста дата публикации установлена в будущем, '
        'отдельная страница такого поста возвращает статус 404.'
    )


def test_posts_page_pk_category_unpublished(
        user_client,
        post_with_unpublished_category,
):
    response = user_client.get(f'/posts/{post_with_unpublished_category.id}/')
    assert response.status_code == HTTPStatus.NOT_FOUND, (
        'Убедитесь, что если посту присвоена категория, снятая с публикации, '
        'то отдельная страница этого поста возвращает статус 404.'
    )


def test_posts_page_pk_post_with_published_location_and_category(
        user_client, post_with_published_location,
        post_context_key
):
    response = user_client.get(
        f'/posts/{post_with_published_location.id}/')
    assert response.status_code == HTTPStatus.OK, (
        'Убедитесь, что если пост не снят с публикации, у него установлена '
        'географическая метка и его категория не снята с публикации - '
        'отдельная страница этого поста существует и отображается.'
    )
    context_post = response.context.get(post_context_key)
    assert context_post == post_with_published_location, (
        'Убедитесь, что в словарь контекста страницы поста '
        f'под ключом `{post_context_key}` '
        'передаётся объект поста c идентификатором `pk`, '
        'где `pk` - параметр строки GET-запроса.'
    )
