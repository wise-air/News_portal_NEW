from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse
from django.core.cache import cache

class Author(models.Model):
    authUser = models.OneToOneField(User, on_delete=models.CASCADE)
    authorRating = models.IntegerField(default=0)

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('postRating'))
        pRat = 0
        pRat += postRat.get('postRating')

        commRat = self.authUser.comment_set.aggregate(commentRating=Sum('commentRating'))
        cRat = 0
        cRat += commRat.get('commentRating')

        self.authorRating = pRat * 3 + cRat
        self.save()

    def __str__(self):
        return '{}'.format(self.authUser)

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Category(models.Model):
    catName = models.CharField(max_length=255, unique=True, verbose_name='Категория')
    subscribers = models.ManyToManyField(User, related_name='categories', blank=True )

    def __str__(self):
        return f'{self.catName.title()}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Post(models.Model):
    article = 'ART'
    news = 'NEW'

    POSITIONS = [
        (article, 'Статья'),
        (news, 'Новость')
    ]
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор публикации')
    typeChoice = models.CharField(max_length=3, choices=POSITIONS, default=news, verbose_name='Вид публикации')
    pubDate = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    postCategory = models.ManyToManyField(Category, through='PostCategory', default="Категория", verbose_name='Категория')
    headline = models.CharField(max_length=255, verbose_name='Заголовок')
    text = models.TextField(default="Текст статьи", verbose_name='Текст')
    postRating = models.SmallIntegerField(default=0, verbose_name='Рейтинг')

    def like(self):
        self.postRating += 1
        self.save()

    def dislike(self):
        self.postRating -= 1
        self.save()

    def preview(self):
        return f'{self.text[0:64]}...'

    def __str__(self):
        return f'{self.headline.title()}: {self.text[:15]}...'

    def get_absolute_url(self):
        return reverse('post_details', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'post-{self.id}')

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    postComm = models.ForeignKey(Post, on_delete=models.CASCADE)
    userComm = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(default='Напишите свой комментарий')
    dateOfComment = models.DateTimeField(auto_now_add=True)
    commentRating = models.SmallIntegerField(default=0)

    def like(self):
        self.commentRating += 1
        self.save()

    def dislike(self):
        self.commentRating += 1
        self.save()

    def __str__(self):
        return f'{self.comment.title()} (User:{self.userComm})'

