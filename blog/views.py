from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from .models import Post
from django.contrib.auth.models import User
# Create your views here.


def home(requests):
    context = {
        'posts': Post.objects.all(),
        'title': 'Home'
    }
    return render(requests, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'  # default is object_list
    ordering = ['-date_posted']  # newest to oldest
    paginate_by = 5
    # paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_post.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'  # newest to oldest
    paginate_by = 5

    def get_queryset(self):
        # get the user or return 404
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        # return the posts of the user
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    # success_url = '/'  # redirects to home page

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    # success_url = '/'  # redirects to home page

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # check if the user is the author of the post
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'  # redirects to home page

    # check if the user is the author of the post
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(requests):
    return render(requests, 'blog/about.html', {'title': 'About'})
