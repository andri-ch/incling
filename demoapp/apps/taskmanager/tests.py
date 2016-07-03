# -*- coding: utf-8 -*-
from django.test import TestCase

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from . import models


# Create your tests here.
class TestProfileModel(TestCase):

    def test_profile_creation(self):
        User = get_user_model()
        # New user created
        user = User.objects.create(
            username="taskbuster", password="django-tutorial")
        # Check that a profile instance has been created
        self.assertIsInstance(user.profile, models.Profile)
        # Call the save method to activate the signal
        # again, and check that it doesn't create another profile instance
        user.save()
        self.assertIsInstance(user.profile, models.Profile)


class TestProjectModel(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create(
            username="taskbuster", password="django-tutorial")
        self.profile = self.user.profile

    def tearDown(self):
        self.user.delete()

    def test_validation_color(self):
        # This first project uses the default value, #fff
        project = models.Project(
            user=self.profile,
            name="TaskManager"
        )
        self.assertTrue(project.color == "#fff")
        # Validation shouldn't rise an Error
        project.full_clean()

        # Good color inputs, without errors:
        for color in ["#1ca", "#12ad99"]:
            project.color = color
            project.full_clean()

        # Bad color inputs
        for color in ["1ca", "1256AB", "#1", "#12", "#1234",
                      "#12345", "#1234567"]:
            with self.assertRaises(
                    ValidationError,
                    msg="%s didn't raise a ValidationError" % color):
                project.color = color
                project.full_clean()
