from django.test import TestCase, Client
from django.urls import reverse

class TestBlogView(TestCase):
    
    def setUp(self):
        self.client = Client()
        
        
    def test_blog_index_url_successful_response(self):
        url = reverse('blog:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(str(response.content).find("Index"))
        self.assertTemplateUsed(response, template_name = "index.html")