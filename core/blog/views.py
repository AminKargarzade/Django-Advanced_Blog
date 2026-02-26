from django.shortcuts import render
from django.views.generic.base import TemplateView
from .models import Post

# Create your views here.
def indexView(request):
    name = 'Amin'
    context = {'name': name}
    return render(request, 'index.html', context)

class IndexView(TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = 'Amin'
        context['posts'] = Post.objects.all()
        return context