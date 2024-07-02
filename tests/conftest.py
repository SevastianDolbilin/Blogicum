from http import HTTPStatus

import pytest
from django.apps import apps
from django.contrib.auth import get_user_model
from mixer.backend.django import mixer as _mixer

try:
    from blog.models import Category, Location, Post  # noqa:F401
except ImportError:
    raise AssertionError(
        'В приложении `blog` опишите '
        'модели `Post, Category, Location`'
    )
except RuntimeError:
    registered_apps = set(app.name for app in apps.get_app_configs())
    need_apps = {'blog': 'blog', 'pages': 'pages'}
    if not set(need_apps.values()).intersection(registered_apps):
        need_apps = {
            'blog': 'blog.apps.BlogConfig', 'pages': 'pages.apps.PagesConfig'}

    for need_app_name, need_app_conf_name in need_apps.items():
        if need_app_conf_name not in registered_apps:
            raise AssertionError(
                f'Убедитесь, что зарегистрировано приложение {need_app_name}'
            )

pytest_plugins = [
    'fixtures.fixture_data'
]


@pytest.fixture
def mixer():
    return _mixer


@pytest.fixture
def user(mixer):
    User = get_user_model()
    return mixer.blend(User)


@pytest.fixture
def user_client(user, client):
    client.force_login(user)
    return client


@pytest.fixture
def post_context_key(user_client, post_with_published_location):
    check_post_page_msg = (
        'Убедитесь, что страница публикации '
        'существует и отображается в соответствии с заданием.'
    )
    try:
        post_response = user_client.get(
            f'/posts/{post_with_published_location.id}/')
    except Exception:
        raise AssertionError(check_post_page_msg)
    assert post_response.status_code == HTTPStatus.OK, check_post_page_msg
    post_key = None
    for key, val in dict(post_response.context).items():
        if isinstance(val, Post):
            post_key = key
            break
    assert post_key, (
        'Убедитесь, что в контекст страницы поста передан объект поста.'
    )
    return post_key


def get_post_list_context_key(
        user_client, page_url, page_load_err_msg, key_missing_msg):
    try:
        post_response = user_client.get(page_url)
    except Exception:
        raise AssertionError(page_load_err_msg)
    assert post_response.status_code == HTTPStatus.OK, page_load_err_msg
    post_list_key = None
    for key, val in dict(post_response.context).items():
        try:
            assert isinstance(iter(val).__next__(), Post)
            post_list_key = key
            break
        except Exception:
            pass
    assert post_list_key, key_missing_msg
    return post_list_key


@pytest.fixture
def main_page_post_list_context_key(mixer, user_client):
    temp_category = mixer.blend('blog.Category', is_published=True)
    temp_location = mixer.blend('blog.Location', is_published=True)
    temp_post = mixer.blend('blog.Post', is_published=True,
                            location=temp_location, category=temp_category)
    page_load_err_msg = (
        'Убедитесь, что главная страница существует и отображается '
        'в соответствии с заданием.'
    )
    key_missing_msg = (
        'Убедитесь, что если существует хотя бы один опубликованный пост '
        'с опубликованной категорией и датой публикации в прошлом, '
        'в контекст главной страницы передаётся непустой список постов.'
    )
    try:
        result = get_post_list_context_key(
            user_client, '/', page_load_err_msg, key_missing_msg)
    except Exception as e:
        raise AssertionError(str(e)) from e
    finally:
        temp_post.delete()
        temp_location.delete()
        temp_category.delete()
    return result


@pytest.fixture
def category_page_post_list_context_key(mixer, user_client):
    temp_category = mixer.blend('blog.Category', is_published=True)
    temp_location = mixer.blend('blog.Location', is_published=True)
    temp_post = mixer.blend(
        'blog.Post', is_published=True,
        category=temp_category, location=temp_location)
    page_load_err_msg = (
        'Убедитесь, что страница категории существует и отображается '
        'в соответствии с заданием в случае, '
        'если категория существует и опубликована.'
    )
    key_missing_msg = (
        'Убедитесь, что если существует хотя бы один опубликованный пост '
        'с опубликованной категорией и датой публикации в прошлом, '
        'в контекст страницы категории передаётся непустой список постов.'
    )
    try:
        result = get_post_list_context_key(
            user_client, f'/category/{temp_category.slug}/',
            page_load_err_msg, key_missing_msg)
    except Exception as e:
        raise AssertionError(str(e)) from e
    finally:
        temp_post.delete()
        temp_location.delete()
        temp_category.delete()
    return result


class _TestModelAttrs:

    @property
    def model(self):
        raise NotImplementedError(
            'Override this property in inherited test class')

    def get_parameter_display_name(self, param):
        return param

    def test_model_attrs(self, field, type, params):
        model_name = self.model.__name__
        assert hasattr(self.model, field), (
            f'В модели `{model_name}` укажите атрибут `{field}`.')
        model_field = self.model._meta.get_field(field)
        assert isinstance(model_field, type), (
            f'В модели `{model_name}` у атрибута `{field}` '
            f'укажите тип `{type}`.'
        )
        for param, value_param in params.items():
            display_name = self.get_parameter_display_name(param)
            assert param in model_field.__dict__, (
                f'В модели `{model_name}` для атрибута `{field}` '
                f'укажите параметр `{display_name}`.'
            )
            assert model_field.__dict__.get(param) == value_param, (
                f'В модели `{model_name}` в атрибуте `{field}` '
                f'проверьте значение параметра `{display_name}` '
                'на соответствие заданию.'
            )
