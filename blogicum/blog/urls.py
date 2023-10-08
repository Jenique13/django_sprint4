from django.urls import path
from .views import (
    PostListView, PostDetailView, CategoryPostsView,
    CreatePostView, EditPostView, AddCommentView, EditCommentView,
    UserProfileView, EditProfileView, ChangePasswordView,
    ProfileUpdateView,
    DeletePostView, DeleteCommentView
)

app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='index'),
    path('posts/<int:pk>/',
         PostDetailView.as_view(), name='post_detail'),
    path('category/<slug:category_slug>/',
         CategoryPostsView.as_view(), name='category_posts'),
    path('posts/create/',
         CreatePostView.as_view(), name='create_post'),
    path('posts/<int:pk>/edit/',
         EditPostView.as_view(), name='edit_post'),
    path('posts/<int:pk>/comment/',
         AddCommentView.as_view(), name='add_comment'),
    path('posts/<int:post_id>/comment/<int:pk>/edit/',
         EditCommentView.as_view(), name='edit_comment'),
    path('posts/<int:pk>/delete/',
         DeletePostView.as_view(), name='delete_post'),
    path('profile/<str:username>/',
         UserProfileView.as_view(), name='profile'),
    path('profile/edit/',
         EditProfileView.as_view(), name='edit_profile'),
    path('profile/change_password/',
         ChangePasswordView.as_view(), name='change_password'),
    path('profile/update/',
         ProfileUpdateView.as_view(), name='profile_update'),
    path('posts/<int:post_id>/comment/<int:pk>/delete/',
         DeleteCommentView.as_view(), name='delete_comment'),
]
