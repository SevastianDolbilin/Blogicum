import importlib

import pytest
from django.apps import apps
from django.conf import settings


def test_rus_localization():
    assert hasattr(settings, 'LANGUAGE_CODE'), (
        'В настройках приложения не обнаружен ключ `LANGUAGE_CODE`.'
    )
    assert settings.LANGUAGE_CODE == 'ru-RU', (
        'В настройках приложения значение ключа '
        '`LANGUAGE_CODE` должно быть `ru-RU`.'
    )


def test_blog_in_rus():
    applications = apps.get_app_configs()
    blog_app = list(filter(lambda x: x.name == 'blog', applications))[0]
    assert blog_app.verbose_name == 'Блог', (
        'Приложение `Blog` не локализированно.'
    )


@pytest.mark.parametrize(('n_model', 'n_verbose', 'n_verbose_plural'), [
    ('Category', 'категория', 'Категории'),
    ('Location', 'местоположение', 'Местоположения'),
    ('Post', 'публикация', 'Публикации'),
])
def test_models_translated(n_model, n_verbose, n_verbose_plural):
    models = apps.get_models()
    found_model = [
        model for model in models
        if model._meta.object_name == n_model
    ]
    found_model = found_model[0]
    assert_msg_template = (
        'Убедитесь, что в модели `{n_model}` добавлен подкласс `Meta`, в '
        'котором для параметра `{param_name}` установлено значение в '
        'соответствии с заданием.'
    )
    assert found_model._meta.verbose_name == n_verbose, (
        assert_msg_template.format(n_model=n_model, param_name='verbose_name')
    )
    assert (
        found_model._meta.verbose_name_plural == n_verbose_plural
    ), (
        assert_msg_template.format(n_model=n_model,
                                   param_name='verbose_name_plural')
    )


@pytest.mark.parametrize(('n_model', 'param', 'n_verbose'), [
    ('Category', 'is_published', 'Опубликовано'),
    ('Category', 'title', 'Заголовок'),
    ('Category', 'slug', 'Идентификатор'),
    ('Category', 'description', 'Описание'),
    ('Category', 'created_at', 'Добавлено'),
    ('Location', 'name', 'Название места'),
    ('Location', 'created_at', 'Добавлено'),
    ('Location', 'is_published', 'Опубликовано'),
    ('Post', 'pub_date', 'Дата и время публикации'),
    ('Post', 'text', 'Текст'),
    ('Post', 'author', 'Автор публикации'),
    ('Post', 'category', 'Категория'),
    ('Post', 'location', 'Местоположение'),
    ('Post', 'created_at', 'Добавлено'),
    ('Post', 'is_published', 'Опубликовано'),
])
def test_models_params_translate(n_model, param, n_verbose):
    module = importlib.import_module('blog.models')
    model = getattr(module, n_model)
    field = model._meta.get_field(param)
    assert field.verbose_name == n_verbose, (
        f'Убедитесь, что в модели `{n_model}` значение `verbose_name` '
        f' для атрибута `{param}` '
        'установлено в соответствии с заданием.'
    )


@pytest.mark.parametrize(('n_model', 'param', 'text'), [
    (
        'Category',
        'is_published',
        'Снимите галочку, чтобы скрыть публикацию.'
    ),
    (
        'Category',
        'slug',
        'Идентификатор страницы для URL; '
        'разрешены символы латиницы, цифры, дефис и подчёркивание.'
    ),
    (
        'Post',
        'pub_date',
        'Если установить дату и время в будущем — '
        'можно делать отложенные публикации.'
    ),
])
def test_help_text_translate(n_model, param, text):
    module = importlib.import_module('blog.models')
    model = getattr(module, n_model)
    field = model._meta.get_field(param)
    assert field.help_text == text, (
        f'Убедитесь, что в модели `{n_model}` значение `help_text` '
        f'для атрибута `{param}` '
        'установлено в соответствии с заданием.'
    )
