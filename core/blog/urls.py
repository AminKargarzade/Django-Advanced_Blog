from django.urls import path
from . import views 
from django.views.generic import TemplateView, RedirectView

app_name = "blog"

urlpatterns = [
    path('cbv-index', views.IndexView.as_view(), name='cbv-index'),
    path('go-to-maktabkhooneh/<int:pk>/', views.RedirectToMaktab.as_view(), name='redirect-to-maktabkhooneh'),
    path('post/', views.PostList.as_view(), name='post-list'),
]