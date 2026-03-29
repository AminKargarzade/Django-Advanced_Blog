from django.shortcuts import get_object_or_404, render
from django.views.generic.base import TemplateView, RedirectView
from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView, DeleteView
from .forms import PostForm
from .models import Post
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
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
    
class PostListView(PermissionRequiredMixin, LoginRequiredMixin ,ListView):
    permission_required = 'blog.view_post'
    # model = Post  
    queryset = Post.objects.all() 
    context_object_name = 'posts'
    paginate_by = 2
    ordering = '-id'
    
    # def get_queryset(self):
    #     posts = Post.objects.filter(status=True)
    #     return posts
    
class PostDetailView(LoginRequiredMixin ,DetailView):
    model = Post
   
''' 
class PostCreateView(FormView):
    template_name = 'contact.html'
    form_class = PostForm
    success_url = '/blog/post/'
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
'''
class PostCreateView(LoginRequiredMixin ,CreateView):
    model = Post
    # fields = ['author', 'title', 'content', 'status', 'category', 'published_date'] You can do the same functionality with form classes
    form_class = PostForm
    success_url = '/blog/post/'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class PostEditView(LoginRequiredMixin ,UpdateView):
    model = Post
    form_class = PostForm
    success_url = '/blog/post/'
    
class PostDeleteView(LoginRequiredMixin ,DeleteView):
    model = Post
    success_url = '/blog/post/'
    
@api_view()
def api_post_list_view(request):
    return Response({"name":"Amin"})