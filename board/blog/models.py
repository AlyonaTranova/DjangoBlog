from django.db import models
from django.template.defaultfilters import truncatechars
from django.utils import timezone


class Post(models.Model):
    STATUS_CHOICES = [
        ('a', 'active'),
        ('i', 'inactive')
    ]
    title = models.CharField(max_length=300, verbose_name='заголовок', default='')
    description = models.TextField(default='описание', verbose_name='описание')
    content = models.TextField(default='', verbose_name='содержание')
    publish_date = models.DateTimeField(default=timezone.now, verbose_name='дата публикации')
    edit_date = models.DateTimeField(auto_now=True, verbose_name='дата редактирования')
    keywords = models.CharField(max_length=120, default='', verbose_name='ключевые слова')
    image = models.FileField(null=True, blank=True, verbose_name='добавить изображение')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='a', verbose_name='статус')
    views_count = models.IntegerField(verbose_name='Количество просмотров', default=0)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def increment_view_count(self):
        self.views_count += 1
        self.save()


class Comment(models.Model):
    STATUS_CHOICES = [
        ('d', 'deleted'),
        ('-', 'not_deleted')
    ]
    news = models.ForeignKey(Post, on_delete=models.CASCADE, default='', verbose_name='пост',
                             related_name='comments')
    user_name = models.CharField(max_length=300, verbose_name='имя автора', default='')
    comment = models.TextField(default='', verbose_name='комментарий')
    created = models.DateTimeField(default=timezone.now, verbose_name='дата публикации')
    active = models.BooleanField(default=True, verbose_name='активность')
    moderation_status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='-', verbose_name='статус')

    class Meta:
        db_table = 'posts'
        ordering = ['created']

    def __str__(self):
        return 'Comment by {} on {}'.format(self.comment, self.news)

    @property
    def short_comment(self):
        return truncatechars(self.comment, 15)

