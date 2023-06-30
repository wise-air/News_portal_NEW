from django.core.management.base import BaseCommand, CommandError
from news.models import Post, Category


class Command(BaseCommand):
    help = 'Команда по удалению новостей по одной из категории. \n' \
           'В случае попытки удаления и подтверждения, \n' \
           'все новости из выбранной категории будут удалены безвозвратно'

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        answer = input(f'Вы правда хотите удалить все статьи в категории {options["category"]}? yes/no')

        if answer != 'yes':
            self.stdout.write(self.style.ERROR('Отменено'))
            return
        try:
            category = Category.objects.get(catName=options['category'])
            Post.objects.filter(category=category).delete()
            self.stdout.write(self.style.SUCCESS(f'Succesfully deleted all news from category {category.catName}')) # в случае неправильного подтверждения говорим, что в доступе отказано
        except Post.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Could not find category {category.catName}'))