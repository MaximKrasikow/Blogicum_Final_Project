# Импорт необходимых модулей для работы с админкой и моделями
from django.contrib import admin
from blog.models import Post, Category, Location

# Настройка административной панели для модели Post
class PostAdmin(admin.ModelAdmin):
    # Определение полей, по которым можно будет искать записи в админке
    search_fields = ('title', 'text', 'pub_date')

# Настройка административной панели для модели Category
class CategoryAdmin(admin.ModelAdmin):
    # Определение полей для поиска
    search_fields = ('title', 'description')

# Настройка административной панели для модели Location
class LocationAdmin(admin.ModelAdmin):
    # Определение полей для поиска
    search_fields = ('name',)

# Установка текста, который будет отображаться для пустых значений в админке
admin.site.empty_value_display = 'Не задано'

# Регистрация моделей и их кастомных админ-классов
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
