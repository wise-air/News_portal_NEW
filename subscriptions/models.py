# from django.db import models
# from django.contrib.auth.models import User
# from news.models import Category
#
#
# class Subscription(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions', blank=True)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subscriptions')
#
#     def __str__(self):
#         return f'{self.user}, {self.category}'
#
#     class Meta:
#         verbose_name = 'Подписка'
#         verbose_name_plural = 'Подписки'
