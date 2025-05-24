from django.urls import path
from .api_views import PostListCreateAPIView, ProfileRetrieveUpdateAPIView

urlpatterns = [
    path('posts/', PostListCreateAPIView.as_view(), name='api-posts'),
    path('profile/', ProfileRetrieveUpdateAPIView.as_view(), name='api-profile'),
]
