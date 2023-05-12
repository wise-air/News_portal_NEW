from django.urls import path
from .views import *

urlpatterns = [
    # path('', CategoryListView.as_view(), name='subscriptions'),
    path('<int:id>/', CategoryListView.as_view(), name='categories'),
    path('<int:id>/subscribe', subscribe, name='subscribe'),
    path('<int:id>/unsubscribe', unsubscribe, name='unsubscribe'),
]