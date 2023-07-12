import logging
from datetime import datetime, timedelta
from django.urls import reverse_lazy

from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
# from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import PermissionRequiredMixin

from .models import Post
from .filters import PostFilter
from .forms import PostForm

from django.http import HttpResponse
from django.views import View
from news.tasks import hello

from django.core.cache import cache
from django.utils.translation import gettext as _


class IndexView(View):
    def get(self, request):
        string = _('Hello world')

        return HttpResponse(string)


logger = logging.getLogger('django')


def log_view(request):
    logger.error("Test message of error")

    x = 3
    y = 0 #0  #Для примера отработки стека ошибки, можно попробовать делить на 0

    logger.info(f"The values of x and y are {x} and {y}.")
    try:
        x / y
        logger.info(f"x/y successful with result: {x / y}.")
    except ZeroDivisionError as err:
        logger.error("ZeroDivisionError")#, exc_info=True)

    return HttpResponse("Test!!! Why doesn't work???")


class PostList(ListView):
    model = Post
    ordering = '-pubDate'
    template_name = 'news.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_post'] = None
        return context


class PostSearch(ListView):
    model = Post
    ordering = '-pubDate'
    template_name = 'news.html'
    context_object_name = 'postsearch'
    paginate_by = 4

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_post'] = None
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    pk_url_kwarg = 'id'

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["id"]}',
                        None)

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["id"]}', obj)

        return obj


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'create_news.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.typeChoice = Post.news
        return super().form_valid(form)


class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'create_article.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.typeChoice = Post.article
        return super().form_valid(form)


class NewsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'edit_news.html'
    pk_url_kwarg = 'id'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if self.object.typeChoice == Post.news:
            self.object.save()
        else:
            raise PermissionDenied()
        return super().form_valid(form)

class ArticleUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'edit_article.html'
    pk_url_kwarg = 'id'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if self.object.typeChoice == Post.article:
            self.object.save()
        else:
            raise PermissionDenied()
        return super().form_valid(form)


class NewsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts_list')
    pk_url_kwarg = 'id'

    def form_valid(self, form):
        if self.object.typeChoice == Post.news:
            return super().form_valid(form)
        else:
            raise PermissionDenied()


class ArticleDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts_list')
    pk_url_kwarg = 'id'

    def form_valid(self, form):
        if self.object.typeChoice == Post.article:
            return super().form_valid(form)
        else:
            raise PermissionDenied()


# class IndexView(View):
#     """example to see docstring"""
#     def get(self, request):
#         hello.delay()
#         return HttpResponse('Hello! Finally we got it!')