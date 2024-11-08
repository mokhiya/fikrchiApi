from django.urls import path
from .views import PostListCreateView, PostRetrieveUpdateDestroyView

app_name = 'posts'

urlpatterns = [
    path('note/', PostListCreateView.as_view(), name='post-list-create'),
    path('note/<int:pk>/', PostRetrieveUpdateDestroyView.as_view(), name='post-retrieve-update-destroy'),
]