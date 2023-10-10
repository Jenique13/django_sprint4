from django.db import models
from django.contrib.auth import get_user_model

from .constants import MAX_STR_LENGHT

User = get_user_model()


class PublishedModel(models.Model):
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено',
    )

    class Meta:
        abstract = True


class TitleModel(models.Model):
    title = models.CharField(
        max_length=MAX_STR_LENGHT,
        verbose_name='Заголовок')

    class Meta:
        abstract = True


class Category(PublishedModel, TitleModel):
    description = models.TextField('Описание')
    slug = models.SlugField('Идентификатор', max_length=64, unique=True,
                            help_text='''Идентификатор страницы для URL;
                разрешены символы латиницы, цифры, дефис и подчёркивание.''')

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.title


class Location(PublishedModel):
    name = models.CharField('Название места', max_length=256)

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self) -> str:
        return self.name


class Post(PublishedModel, TitleModel):
    title = models.CharField(
        max_length=200, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        'Дата и время публикации',
        help_text='''Если установить дату и время в будущем,
                     можно делать отложенные публикации.'''
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория'
    )
    image = models.ImageField(upload_to='post_images/', blank=True)

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self) -> str:
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='Автор публикации')
    text = models.TextField('Текст комментария', null=False)
    created_at = models.DateTimeField(auto_now_add=True)
