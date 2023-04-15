from catalog.models import Project
from django.contrib.auth import get_user_model
from django.test import TestCase


class TestModels(TestCase):
    def setUp(self):
        user = get_user_model()
        self.owner = user.objects.create_user(
            username='testuser', password='12345'
        )

    def test_project_create(self):
        act = Project.objects.create(
            owner=self.owner,
            name='Test123',
            description='',
        )
        act.save()
        act.full_clean()
        act.save()
