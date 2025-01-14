from django.apps import AppConfig


class CoreConfig(AppConfig):
    # Устанавливает тип поля для автоматически генерируемых первичных ключей. 
    # В данном случае используется BigAutoField, который позволяет использовать 
    # 64-битные числа для первичных ключей, что дает больше пространства для 
    # записей в базе данных.
    default_auto_field = 'django.db.models.BigAutoField'
    
    # Имя приложения в проекте Django. Это имя должно совпадать с названием 
    # каталога, в котором находится ваше приложение. В данном случае приложение 
    # называется "core".
    name = 'core'
