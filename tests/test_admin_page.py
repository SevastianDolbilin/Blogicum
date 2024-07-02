from django.apps import apps
from django.contrib import admin


def test_admin_register():
    models = apps.get_models()
    for model in models:
        if model._meta.object_name in ('Category', 'Post', 'Location'):
            assert model in admin.site._registry, (
                f'Убедитесь, что модель `{model._meta.object_name}` '
                'зарегистрирована в админке.'
            )
