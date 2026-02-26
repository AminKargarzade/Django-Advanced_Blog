from django.shortcuts import render
from django.views.generic.base import TemplateView
from .models import Post

# Create your views here.
def indexView(request):
    """
    This is a function-based view that renders the 'index.html' template with a context containing a name.
    """
    name = 'Amin'
    context = {'name': name}
    return render(request, 'index.html', context)

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