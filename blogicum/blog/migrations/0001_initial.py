import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID')),
                ('is_published', models.BooleanField(
                    default=True,
                    verbose_name='Опубликовано')),
                ('created_at', models.DateTimeField(
                    auto_now_add=True,
                    help_text='Снимите галочку, чтобы\n скрыть публикацию.',
                    verbose_name='Добавлено')),
                ('title', models.CharField(
                    max_length=256,
                    verbose_name='Заголовок')),
                ('description', models.TextField(
                    verbose_name='Описание')),
                ('slug', models.SlugField(
                    help_text=(
                        'Идентификатор страницы для URL;\n разрешены '
                        'символы латиницы, цифры, дефис и подчёркивание.'),
                    max_length=64, unique=True, verbose_name='Идентификатор')),
            ],
            options={
                'verbose_name': 'категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID')),
                ('is_published', models.BooleanField(
                    default=True,
                    verbose_name='Опубликовано')),
                ('created_at', models.DateTimeField(
                    auto_now_add=True,
                    help_text='Снимите галочку, чтобы\n скрыть публикацию.',
                    verbose_name='Добавлено')),
                ('name', models.CharField(max_length=256,
                                          verbose_name='Название места')),
            ],
            options={
                'verbose_name': 'местоположение',
                'verbose_name_plural': 'Местоположения',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID')),
                ('is_published', models.BooleanField(
                    default=True,
                    verbose_name='Опубликовано')),
                ('created_at', models.DateTimeField(
                    auto_now_add=True,
                    help_text='Снимите галочку, чтобы\n скрыть публикацию.',
                    verbose_name='Добавлено')),
                ('title', models.CharField(
                    max_length=256,
                    verbose_name='Заголовок')),
                ('text', models.TextField(
                    verbose_name='Текст')),
                ('pub_date', models.DateTimeField(
                    help_text=(
                        'Если установить дату и время в будущем,\n можно '
                        'делать отложенные публикации.'),
                    verbose_name='Дата и время публикации')),
                ('author', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(
                    null=True, on_delete=django.db.models.deletion.SET_NULL,
                    to='blog.category')),
                ('location', models.ForeignKey(
                    null=True, on_delete=django.db.models.deletion.SET_NULL,
                    to='blog.location')),
            ],
            options={
                'verbose_name': 'публикация',
                'verbose_name_plural': 'Публикации',
            },
        ),
    ]
