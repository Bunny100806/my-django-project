from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework.authtoken.views import obtain_auth_token

# DRF router for API endpoints
router = DefaultRouter()
router.register(r'posts', views.PostViewSet, basename='post')

urlpatterns = [
    # HTML views
    path('', views.feed, name='feed'),
    path('home/', views.home, name='home'),  # optional home page
    path('register/', views.register, name='register'),
    path('profile/', views.profile_detail, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('accounts/profile/', views.profile_redirect, name='profile_redirect'),

    # Post HTML views
    path('posts/', views.post_list, name='post_list'),
    path('posts/add/', views.post_create, name='post_create'),
    path('posts/<int:pk>/', views.post_detail, name='post_detail'),
    path('posts/<int:pk>/edit/', views.post_update, name='post_update'),
    path('posts/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('post/create/', views.post_create, name='create_post'),


    # DRF Auth token
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),

    # DRF API router URLs
    path('api/', include(router.urls)),
]
