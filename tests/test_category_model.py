import pytest
from django.db.models import (
    BooleanField, CharField, SlugField, TextField, DateTimeField)

from blog.models import Category
from tests.conftest import _TestModelAttrs


@pytest.mark.parametrize(('field', 'type', 'params'), [
    ('title', CharField, {'max_length': 256}),
    ('description', TextField, {}),
    ('slug', SlugField, {'_unique': True}),
    ('is_published', BooleanField, {'default': True}),
    ('created_at', DateTimeField, {'auto_now_add': True}),
])
class TestCategoryModelAttrs(_TestModelAttrs):

    def get_parameter_display_name(self, param):
        return 'unique' if param == '_unique' else param

    @property
    def model(self):
        return Category
