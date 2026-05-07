from django.test import TestCase
from datetime import datetime

from ..models import Post, Category
from django.contrib.auth import get_user_model
from accounts.models import User, Profile

class TestPostModel(TestCase):
    
    def test_create_post_with_valid_data(self):
        user = User.objects.create_user(email="test@test.com", password="a/@1234567") # type: ignore
        profile = Profile.objects.create(
            user = user,
            first_name = "test_first_name",
            last_name = "test_last_name",
            description = "test_description",
        )
        post = Post.objects.create(
            author = profile,
            title = "test",
            content = "description",
            status = True,
            category = None,
            published_date = datetime.now(),
        )
        self.assertEqual(post.title, "test")