from catalog.models import Project
from django.contrib.auth.models import User
from django.test import TestCase


class TestModels(TestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            username='testuser',
            password='12345'
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
