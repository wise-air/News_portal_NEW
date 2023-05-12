from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.views.decorators.csrf import csrf_protect
from django.views.generic import (ListView)
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


# @login_required
# @csrf_protect
# def subscriptions(request):
#
#     if request.method == 'POST':
#         category_id = request.POST.get('category_id')
#         category = Category.objects.get(id=category_id)
#         action = request.POST.get('action')
#
#         user = request.user
#         # if not Subscription.objects.filter(id=user.id).exists():
#         #     Category.objects.create(subscribers=user.username, catName=category)
#
#
#         if action == 'subscribe':
#             Category.objects.create(subscribers=user)#, catName=category)
#         elif action == 'unsubscribe':
#             Category.objects.filter(
#                 subscribers=user,
#             ).delete()
#
#
#     categories_with_subscriptions = Category.objects.annotate(
#         user_subscribed=Exists(
#             Category.objects.filter(
#                 subscribers=request.user,
#                 catName=OuterRef('id'),
#             )
#         )
#     ).order_by('catName')
#     return render(
#         request,
#         'subscriptions.html',
#         {'categories': categories_with_subscriptions},
#     )