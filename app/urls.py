from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.authtoken import views
from .views_social import GitHubLogin
from .views import (
    PostListAPIView,
    PostCreateAPIView,
    PostRetrieveAPIView,
    PostUpdateAPIView,
    PostDestroyAPIView,
    PostListCreateAPIView,
    PostRetrieveUpdateAPIView,
    PostRetrieveDestroyAPIView,
    PostRetrieveUpdateDestroyAPIView,
    PostViewSet,
    CategoryViewSet,
)

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    # Generic API views 
    path('posts/list/', PostListAPIView.as_view(), name='post-list'),
    path('posts/create/', PostCreateAPIView.as_view(), name='post-create'),
    path('posts/<int:pk>/', PostRetrieveUpdateDestroyAPIView.as_view(), name='post-retrieve-update-delete'),
    path('posts/update/<int:pk>/', PostUpdateAPIView.as_view(), name='post-update'),
    path('posts/delete/<int:pk>/', PostDestroyAPIView.as_view(), name='post-delete'),

    # Combined generic views
    path('posts/list-create/', PostListCreateAPIView.as_view(), name='post-list-create'),
    path('posts/retrieve-update/<int:pk>/', PostRetrieveUpdateAPIView.as_view(), name='post-retrieve-update'),
    path('posts/retrieve-delete/<int:pk>/', PostRetrieveDestroyAPIView.as_view(), name='post-retrieve-delete'),
    path('posts/retrieve-update-delete/<int:pk>/', PostRetrieveUpdateDestroyAPIView.as_view(), name='post-retrieve-update-delete'),

    # ViewSet URLs
    path('', include(router.urls)),

    path('auth-token/'  , views.obtain_auth_token, name='api_token_auth'), 
    path('github/', GitHubLogin.as_view(), name='github_login'),
  
]