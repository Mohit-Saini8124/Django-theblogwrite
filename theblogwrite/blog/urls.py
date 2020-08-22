from django.urls import path
from .views import (
                    Dashboard,
                    BlogSearchView,
                    BlogPostListView,
                    CategoryPostListView,
                    UserPostListView,
                    BlogPostDetailView,
                    BlogPostCreateView,
                    BlogPostUpdateView,
                    BlogPostDeleteView
                    ) 


urlpatterns = [
    path('', BlogPostListView.as_view(), name='mainblog'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-related-post'),
    path('ctgry/<str:title>', CategoryPostListView.as_view(), name='category-related-post'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('search/', BlogSearchView.as_view(), name='BlogSearchResult'),
    path('<int:pk>/<slug:slug>/', BlogPostDetailView.as_view(), name='post-detail'),
    path('post/new/', BlogPostCreateView.as_view(), name='post-create'),
    path('<int:pk>/<slug:slug>/update/', BlogPostUpdateView.as_view(), name='post-update'),
    path('<int:pk>/<slug:slug>/delete/', BlogPostDeleteView.as_view(), name="post-delete"),
    
    ] 
