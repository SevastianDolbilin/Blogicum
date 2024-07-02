from http import HTTPStatus

import pytest
from pytest_django.asserts import assertTemplateUsed


@pytest.mark.parametrize('page', ('about', 'rules'))
@pytest.mark.django_db
def test_pageapp_views(user_client, page):
    response = user_client.get(f'/pages/{page}/')
    assert response.status_code == HTTPStatus.OK, (
        f'Убедитесь, что страница `/pages/{page}/` существует и отображается '
        'в соответствии с заданием.'
    )
    try:
        assertTemplateUsed(response, f'pages/{page}.html')
    except AssertionError:
        raise AssertionError(
            f'Для страницы`/pages/{page}/` '
            f'используйте шаблон `pages/{page}.html`'
        )
