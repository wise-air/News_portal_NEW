from django.contrib import admin
from .models import Author, Post, Comment, Category


def nullfy_rating(modeladmin, request, queryset):
    queryset.update(postRating=0)
nullfy_rating.short_description = 'Обнулить рейтинг'


class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'pubDate', 'headline', 'typeChoice', 'preview', 'postRating')
    list_filter = ('pubDate', 'typeChoice')
    search_fields = ('headline', 'text')
    actions = [nullfy_rating]

admin.site.register(Author)
admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Comment)
