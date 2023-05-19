from news.filters import PostFilter
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView
from news.models import *



class CategoryListView(ListView):
    model = Post
    template_name = 'categories.html'
    context_object_name = 'category_list_news'

    def get_queryset(self):
        self.postCategory = get_object_or_404(Category, id=self.kwargs['id']) #8:15
        queryset = Post.objects.filter(postCategory=self.postCategory).order_by('-pubDate')
        return queryset

    def get_context_data(self , **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.postCategory.subscribers.all()
        context['category'] = self.postCategory
        return context

@login_required
def subscribe(request, id):
    user = request.user
    category = Category.objects.get(id=id)
    category.subscribers.add(user)

    message = 'Вы успешно подписались на рассылку '
    return render(request, 'subscribe.html', {'category': category, 'message': message})

@login_required
def unsubscribe(request, id):
    user = request.user
    category = Category.objects.get(id=id)
    category.subscribers.remove(user)

    message = 'Вы успешно отписались от рассылки '
    return render(request, 'unsubscribe.html', {'category': category, 'message': message})



class SubscriptionsListView(ListView):
    model = Category
    template_name = 'subscriptions.html'
    context_object_name = 'subscribe_list'

    def get_queryset(self):
        category = ", ".join(Category.objects.filter(subscribers=self.request.user).values_list('catName', flat= True))
        return category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.catName
        return context