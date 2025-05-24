from django.test import TestCase
from core.models import Post

class PostModelTest(TestCase):
    def test_create_post(self):
        post = Post.objects.create(title="Test", content="Hello")
        self.assertEqual(post.title, "Test")