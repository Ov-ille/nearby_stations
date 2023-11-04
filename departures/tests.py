from django.contrib.auth.models import User
from django.apps import apps
import pytest

# Create your tests here.


@pytest.mark.django_db
class Test_db:
    def test_models_exist(self):
        assert "Stations" in [x.__name__ for x in apps.get_models()]
