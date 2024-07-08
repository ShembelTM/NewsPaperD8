from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, PostCategory
from datetime import datetime
from .filters import PostFilter
from .forms import NewsForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin


class PostsList(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'news.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context


class NewsFilter(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'search_news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()

        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('news.add_post',
                           'news.change_post',
                           'news.delete_post',)
    form_class = NewsForm
    model = Post
    template_name = 'edit_news.html'
    success_url = reverse_lazy('news_list')
    raise_exception = True

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'news'
        post.save()
        return super().form_valid(form)


class ArticleCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('news.add_post',
                           'news.change_post',
                           'news.delete_post',)
    form_class = NewsForm
    model = Post
    template_name = 'edit_news.html'
    success_url = reverse_lazy('news_list')
    raise_exception = True

    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_type = 'article'
        post.save()
        return super().form_valid(form)


class NewsUpdate(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    permission_required = ('news.add_post',
                           'news.change_post',
                           'news.delete_post',)
    form_class = NewsForm
    model = Post
    template_name = 'edit_news.html'
    success_url = reverse_lazy('news_list')
    raise_exception = True


class NewsDelete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = ('news.add_post',
                           'news.change_post',
                           'news.delete_post',)
    form_class = NewsForm
    model = Post
    template_name = 'delete_news.html'
    success_url = reverse_lazy('news_list')
    raise_exception = True


class PostsDetail(DetailView):
    model = Post
    template_name = 'news1.html'
    context_object_name = 'news1'
