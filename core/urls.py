from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile_detail, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('accounts/profile/', views.profile_redirect),

    # Posts
    path('posts/', views.post_list, name='post_list'),
    path('add/', views.post_create, name='post_create'),
    path('<int:pk>/', views.post_detail, name='post_detail'),
    path('<int:pk>/edit/', views.post_update, name='post_update'),
    path('<int:pk>/delete/', views.post_delete, name='post_delete'),
]
