from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

from core.models import PublishedModel

# Получение модели пользователя
User = get_user_model()

# Модель категории, наследующая от PublishedModel
class Category(PublishedModel):
    # Заголовок категории (максимальная длина — 256 символов)
    title = models.CharField(max_length=256, verbose_name='Заголовок')
    # Описание категории (текстовое поле)
    description = models.TextField(verbose_name='Описание')
    # Фото категории (не обязательное поле, используется для загрузки изображений)
    image = models.ImageField('Фото', upload_to='post_images', blank=True)
    # Уникальный идентификатор для URL (с помощью slug)
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text='Идентификатор страницы для URL; '
                  'разрешены символы латиницы, цифры, дефис и подчёркивание.',
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title

# Модель местоположения, также наследует от PublishedModel
class Location(PublishedModel):
    # Название места (максимальная длина — 256 символов)
    name = models.CharField(max_length=256, verbose_name='Название места')

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name

# Модель поста, наследует от PublishedModel
class Post(PublishedModel):
    # Заголовок поста (максимальная длина — 256 символов)
    title = models.CharField(max_length=256, verbose_name='Заголовок')
    # Текст поста (основное содержание публикации)
    text = models.TextField(verbose_name='Текст')
    # Фото поста (не обязательное поле, используется для загрузки изображений)
    image = models.ImageField('Фото', upload_to='post_images', blank=True)
    # Дата и время публикации
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text='Если установить дату и время в будущем — '
                  'можно делать отложенные публикации.',
    )
    # Автор публикации (внешний ключ к модели User, удаление записи приводит к удалению постов)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
        related_name='posts',
    )
    # Местоположение, с которым связана публикация (внешний ключ к модели Location)
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Местоположение',
        related_name='posts',
    )
    # Категория, к которой относится публикация (внешний ключ к модели Category)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
        related_name='posts',
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)

    # Метод для получения абсолютного URL поста (используется для перенаправлений)
    def get_absolute_url(self):
        return reverse('blog:profile', args=[self.author])

    # Метод для подсчета количества комментариев
    def comment_count(self):
        return self.comments.count()

    def __str__(self):
        return self.title

# Модель комментария, связана с моделью Post
class Comment(models.Model):
    # Текст комментария
    text = models.TextField('Текст комментария')
    # Пост, к которому привязан комментарий (внешний ключ к модели Post)
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пост',
        help_text='Выберите пост, к которому относится комментарий',
    )
    # Время создания комментария
    created_at = models.DateTimeField(auto_now_add=True)
    # Автор комментария (внешний ключ к модели User)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author',
    )

    class Meta:
        ordering = ('created_at',)
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text

# Модель профиля пользователя, также наследует от PublishedModel
class Profile(PublishedModel):
    # Имя пользователя
    first_name = models.CharField(max_length=30, blank=True)
    # Фамилия пользователя
    last_name = models.CharField(max_length=30, blank=True)
    # Электронная почта пользователя
    email = models.EmailField(blank=True)
    # Адрес пользователя
    address = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.title
