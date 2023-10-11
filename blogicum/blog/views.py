from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone as dt
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)

# from django.views.generic.list import MultipleObjectMixin

from django.urls import reverse_lazy
from django.http import Http404
from django.contrib.auth.models import User
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    UpdateView,
    DetailView
)
from django.db.models import Count


from .models import Post, Comment, Category
from .forms import PostForm, CommentForm, ProfileForm


class PostListView(ListView):
    model = Post
    paginate_by = 10
    template_name = 'blog/index.html'

    def get_queryset(self):
        queryset = Post.objects.annotate(
            comment_count=Count('comments')).filter(
            pub_date__lte=dt.now(),
            is_published=True,
            category__is_published=True
        ).order_by('-pub_date')

        return queryset


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    pk_url_kwarg = 'post_id'
    template_name = 'blog/create.html'
    login_url = '/auth/login/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.pub_date = form.cleaned_data['pub_date']
        return super().form_valid(form)

    def save(self):
        post = super().save()
        return post

    def get_success_url(self):
        username = self.request.user.username
        return reverse_lazy('blog:profile', kwargs={'username': username})


class PostDetailView(DetailView):
    model = Post
    pk_url_kwarg = 'post_id'
    template_name = 'blog/detail.html'

    def get_object(self):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        if post.author == self.request.user:
            return post

        if not post.is_published:
            raise Http404

        if not post.category.is_published:
            raise Http404

        if post.pub_date > dt.now():
            raise Http404

        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comments.select_related('author')
        return context


class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    login_url = '/auth/login/'
    pk_url_kwarg = 'post_id'

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            return redirect('blog:post_detail', self.get_object().pk)
        get_object_or_404(Post, pk=kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)

    def has_permission(self):
        post = self.get_object()
        return self.request.user == post.author

    def get_success_url(self):
        return reverse_lazy('blog:post_detail',
                            kwargs={'post_id': self.object.pk})


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/create.html'
    login_url = '/auth/login/'
    success_url = reverse_lazy('blog:index')
    pk_url_kwarg = 'post_id'

    def get_queryset(self):
        return Post.objects.filter(
            author=self.request.user, pk=self.kwargs['post_id'])

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset,)
        if obj.author != self.request.user:
            raise PermissionDenied
        return obj


# class CategoryDetailView(MultipleObjectMixin, DetailView):
#    model = Category
#    slug_url_kwarg = 'category_slug'
#    paginate_by = 10
#    template_name = 'blog/category.html'
#
#    def get_object(self):
#        return get_object_or_404(
#            Category,
#            slug=self.kwargs['category_slug'],
#            is_published=True,
#        )
#
#    def get_context_data(self, **kwargs):
#        return super().get_context_data(
#            object_list=Post.objects.annotate(
#                comment_count=Count(
#                    'comments')).filter(
#                        pub_date__lte=dt.now(),
#                        is_published=True,
#                        category=self.object,
#                        category__is_published=True).order_by(
#                            '-pub_date'), **kwargs)


class CategoryListView(ListView):
    model = Category
    template_name = 'blog/category.html'
    context_object_name = 'post_list'
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        self.category = get_object_or_404(
            Category,
            slug=kwargs['category_slug'],
            is_published=True,
        )
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Post.objects.select_related(
            'author',
            'location',
            'category',
        ).filter(
            is_published=True,
            category=self.category,
            pub_date__lte=dt.now(),
        ).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class UserListView(ListView):
    template_name = 'blog/profile.html'
    slug_url_kwarg = 'username'
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.username != self.kwargs['username']:
            queryset = Post.objects.select_related(
                'author',
                'location'
            ).annotate(comment_count=Count('comments')).filter(
                pub_date__lt=dt.now(),
                is_published__exact=True,
                author__username=self.kwargs['username']
            ).order_by('-pub_date')
        else:
            queryset = Post.objects.select_related(
                'author',
                'location'
            ).annotate(comment_count=Count('comments')).filter(
                author__username=self.kwargs['username']
            ).order_by('-pub_date')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(
            User,
            username=self.kwargs['username'])
        return context


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'blog/user.html'

#    def dispatch(self, request, *args, **kwargs):
#        self.user_object = get_object_or_404(
#            User,
#            username=self.kwargs.get('username'))
#        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        return self.request.user
#        user = super().get_object()
#        if not self.request.user == user:
#            raise Http404('У вас нет доступа к
# редактированию этой информации')
#        return user

    def get_success_url(self):
        return reverse_lazy(
            'blog:profile', kwargs={'username': self.request.user.username})


class PasswordUpdateView(UpdateView):
    template_name = 'change_password.html'
    success_url = reverse_lazy('login')


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'
    login_url = '/auth/login/'
    pk_url_kwarg = 'post_id'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'blog:post_detail', kwargs={'post_id': self.kwargs['post_id']})


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def get_object(self):
        comment = get_object_or_404(Comment, pk=self.kwargs['comment_id'])
        if comment.author != self.request.user:
            raise PermissionDenied
        return comment

    def get_success_url(self):
        return reverse(
            'blog:post_detail', kwargs={'post_id': self.kwargs['post_id']})


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def get_object(self):
        comment = get_object_or_404(Comment, pk=self.kwargs['comment_id'])
        if comment.author != self.request.user:
            raise PermissionDenied
        return comment

    def get_success_url(self):
        return reverse(
            'blog:post_detail', kwargs={'post_id': self.kwargs['post_id']})
