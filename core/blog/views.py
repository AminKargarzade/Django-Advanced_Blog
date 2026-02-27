from django.shortcuts import get_object_or_404, render
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic import ListView
from .models import Post
from django.shortcuts import get_object_or_404
# Create your views here.

# Function-based view to Show a template with a context
'''
def indexView(request):
    """
    This is a function-based view that renders the 'index.html' template with a context containing a name.
    """
    name = 'Amin'
    context = {'name': name}
    return render(request, 'index.html', context)
'''
class IndexView(TemplateView):
    """
    This is a class-based view that renders the 'index.html' template with a context containing a name and a list of posts.
    """
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Amin'
        context['posts'] = Post.objects.all()
        return context
    
# FBV for RedirectView
'''
from django.shortcuts import redirect
def redirectToMaktab(request):
    """
    This is a function-based view that redirects the user to the Maktabkhooneh website.
    """
    return redirect('https://maktabkhooneh.org/')
'''

class RedirectToMaktab(RedirectView):
    """
    This is a class-based view that redirects the user to the Maktabkhooneh website.
    """
    url = 'https://maktabkhooneh.org/'
    
    def get_redirect_url(self, *args, **kwargs):
        return super().get_redirect_url(*args, **kwargs)
    
class PostList(ListView):
    # model = Post | you can use it instead of queryset
    # queryset = Post.objects.all() | you can use it instead of model
    
    def get_queryset(self):
        posts = Post.objects.filter(status=True)
        return posts
    
    context_object_name = 'posts'
    