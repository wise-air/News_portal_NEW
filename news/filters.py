from django_filters import FilterSet, DateTimeFilter, \
                            ModelChoiceFilter, ModelMultipleChoiceFilter
from django.forms import DateTimeInput
from .models import Post, User, Category


class PostFilter(FilterSet):
    added_after = DateTimeFilter(
        field_name='pubDate',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        ),
    )

    author_filter = ModelChoiceFilter(
        field_name='author__authUser__username',
        # lookup_expr='iregex',
        queryset=User.objects.all(),
        label='Автор статьи',
        empty_label='ВСЕ',


    )

    category_filter = ModelMultipleChoiceFilter(
        field_name='postcategory__categoryThrough__catName',
        # lookup_expr='iregex',
        queryset=Category.objects.all(),
        label='Категория публикации',
        conjoined=True,
    )

    class Meta:
       model = Post
       fields = {
           'headline': ['iregex'],
           # 'typeChoice': ['icontains'],
       }