from django.urls import path
from .views import PostDetailView, PostListView, About

urlpatterns = [
    path('', PostListView.as_view(), name='blog'),
    path('about', About.as_view(), name='about'),
    path('<int:pk>', PostDetailView.as_view(), name='blog-detail'),
]
