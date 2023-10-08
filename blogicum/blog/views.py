import datetime
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import Http404
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.models import User
from django.views.generic.list import ListView
from django.http import HttpResponseServerError
from django.db.models import Count

from .models import Post, Comment, Category
from .forms import PostForm, CommentForm, EditCommentForm, ProfileForm


class IndexView(View):
    template_name = 'blog/index.html'
    paginate_by = 10

    def get(self, request):
        posts = Post.objects.annotate(num_comments=Count('comments')).filter(
            pub_date__lte=datetime.datetime.now(),
            is_published=True,
            category__is_published=True
        ).order_by('-pub_date')

        paginator = Paginator(posts, self.paginate_by)
        page = request.GET.get('page')
        posts = paginator.get_page(page)

        context = {'posts': posts, 'num_comments': posts.num_comments}
        return render(request, self.template_name, context)


class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    login_url = '/auth/login/'
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.pub_time = form.cleaned_data['pub_time']
        return super().form_valid(form)

    def save(self):
        post = super().save()
        return post


class EditPostView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    login_url = '/auth/login/'

    def get(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        if request.user != post.author:
            return redirect('blog:index')
        form = PostForm(instance=post)
        return render(request, self.template_name,
                      {'form': form, 'post': post})

    def post(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        if request.user != post.author:
            return redirect('blog:index')
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', pk=pk)
        return render(request, self.template_name,
                      {'form': form, 'post': post})


class AddCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'
    login_url = '/auth/login/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        post_id = self.kwargs['pk']

        post = get_object_or_404(Post, id=post_id)

        form.instance.post = post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blog:post_detail',
                            kwargs={'pk': self.kwargs['pk']})


class EditCommentView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = EditCommentForm
    template_name = 'blog/comment.html'
    login_url = '/auth/login/'

    def get_object(self, queryset=None):
        comment = super().get_object(queryset)
        if self.request.user != comment.author:
            raise Http404()
        return comment

    def form_valid(self, form):
        post_id = self.kwargs.get('post_id')
        if post_id is None:
            raise Http404("post_id не найден в URL")

        comment = form.save(commit=False)
        comment.post_id = post_id
        comment.save()

        return redirect('blog:post_detail', pk=post_id)


class PostListView(ListView):
    model = Post
    paginate_by = 10
    queryset = Post.objects.annotate(num_comments=Count('comments')).filter(
            pub_date__lte=datetime.datetime.now(),
            is_published=True,
            category__is_published=True).order_by('-pub_date')
    template_name = 'blog/index.html'
    context_object_name = 'page_obj'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['num_comments'] = self.queryset.aggregate(
            num_comments=Count('comments'))['num_comments']
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'

    def get_object(self, queryset=None):
        return get_object_or_404(
            Post.objects.select_related('author', 'category', 'location')
            .filter(
                pub_date__lte=datetime.datetime.now(),
                is_published=True,
                category__is_published=True
            ),
            id=self.kwargs['pk']
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comments.select_related('author')
        return context


class UserProfileView(View):
    template_name = 'blog/profile.html'
    paginate_by = 10

    def get(self, request, username):
        try:
            user = get_object_or_404(User, username=username)
            posts = Post.objects.filter(author=user).order_by('-pub_date')
            paginator = Paginator(posts, self.paginate_by)
            page = request.GET.get('page')

            posts = paginator.get_page(page)

            context = {
                'profile_user': user,
                'user': self.request.user,
                'page_obj': posts,
            }
            return render(request, self.template_name, context)
        except Exception as e:
            return HttpResponseServerError(f"An error occurred: {str(e)}")


class EditProfileView(UpdateView):
    model = User
    template_name = 'edit_profile.html'
    fields = ['first_name', 'last_name', 'email', 'username']
    success_url = reverse_lazy('user_profile')

    def get_object(self, queryset=None):
        return self.request.user


class ChangePasswordView(PasswordChangeView):
    template_name = 'change_password.html'
    success_url = reverse_lazy('login')


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = 'blog/user.html'
    slug_url_kwarg = 'username'
    slug_field = 'username'

    def get_object(self):
        user = super().get_object()
        if not self.request.user == user:
            raise Http404('У вас нет доступа к редактированию этой информации')
        return user


class DeletePostView(DeleteView):
    model = Post
    template_name = 'blog/delete_post.html'
    success_url = reverse_lazy('blog:index')


class CategoryPostsView(View):
    template_name = 'blog/category.html'
    paginate_by = 10

    def get(self, request, category_slug):
        category = Category.objects.get(slug=category_slug)
        posts = Post.objects.filter(
            category=category,
            pub_date__lte=datetime.datetime.now(),
            is_published=True,
        ).order_by('-pub_date')

        paginator = Paginator(posts, self.paginate_by)
        page = request.GET.get('page')
        posts = paginator.get_page(page)

        context = {
            'category': category,
            'posts': posts,
        }

        return render(request, self.template_name, context)


class DeleteCommentView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment.html'
    success_url = '/'

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        comment = self.get_object()
        if request.user == comment.author:
            comment.delete()
        return redirect(self.success_url)
