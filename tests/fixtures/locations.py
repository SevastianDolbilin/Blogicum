import pytest
from conftest import N_PER_FIXTURE
from mixer.backend.django import Mixer


@pytest.fixture
def published_locations(mixer: Mixer):
    return mixer.cycle(N_PER_FIXTURE).blend("blog.Location")


@pytest.fixture
def published_location(mixer: Mixer):
    return mixer.blend("blog.Location", is_published=True)
