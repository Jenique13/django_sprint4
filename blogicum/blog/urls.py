from django.urls import path
from .views import (
    PostListView, PostCreateView, PostDetailView,
    PostUpdateView, PostDeleteView,
    CategoryListView,
    UserListView, UserUpdateView, PasswordUpdateView,
    CommentCreateView, CommentUpdateView, CommentDeleteView
)

app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='index'),
    path('posts/create/',
         PostCreateView.as_view(), name='create_post'),
    path('posts/<int:post_id>/edit/',
         PostUpdateView.as_view(), name='edit_post'),
    path('posts/<int:post_id>/',
         PostDetailView.as_view(), name='post_detail'),
    path('posts/<int:post_id>/delete/',
         PostDeleteView.as_view(), name='delete_post'),

    path('category/<slug:category_slug>/',
         CategoryListView.as_view(), name='category_posts'),

    path('profile/change_password/',
         PasswordUpdateView.as_view(), name='password_change'),
    path('profile/update/',
         UserUpdateView.as_view(), name='edit_profile'),
    path('profile/<slug:username>/',
         UserListView.as_view(), name='profile'),


    path('posts/<int:post_id>/comment/',
         CommentCreateView.as_view(), name='add_comment'),
    path('posts/<int:post_id>/edit_comment/<int:comment_id>/edit/',
         CommentUpdateView.as_view(), name='edit_comment'),
    path('posts/<int:post_id>/comment/<int:pk>/delete/',
         CommentDeleteView.as_view(), name='delete_comment'),
]
