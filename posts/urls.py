from django.urls import path, include
from posts import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('post/<slug:slug>', views.PostDetailView.as_view(), name='post_detail'),
    path("category/<slug:slug>", views.CategoryDetailView.as_view(), name='category_posts'),
]