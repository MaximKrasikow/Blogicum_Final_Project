# Импорт моделей Django, включая модель AbstractUser, которая предоставляет базовую структуру для пользователей.
from django.db import models
from django.contrib.auth.models import AbstractUser

# Кастомная модель пользователя, расширяющая AbstractUser
class MyUser(AbstractUser):
    # Дополнительное поле 'bio' для хранения биографии пользователя.
    bio = models.TextField('Биография', blank=True)
