from django.urls import path

from .views import PostList, PostSearch, PostDetail, NewsCreate, NewsUpdate, NewsDelete, ArticleCreate, ArticleUpdate, ArticleDelete


urlpatterns = [
   path('', PostList.as_view(), name='posts_list'),
   path('search/', PostSearch.as_view(), name='post_search'),
   path('<int:id>', PostDetail.as_view(), name='post_details'),
   path('NEW/create/', NewsCreate.as_view(), name='news_create'),
   path('ART/create/', ArticleCreate.as_view(), name='article_create'),
   path('NEW/<int:id>/update/', NewsUpdate.as_view(), name='news_update'),
   path('ART/<int:id>/update/', ArticleUpdate.as_view(), name='article_update'),
   path('NEW/<int:id>/delete/', NewsDelete.as_view(), name='news_delete'),
   path('ART/<int:id>/delete/', ArticleDelete.as_view(), name='article_delete'),


]