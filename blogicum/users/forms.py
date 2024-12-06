# Импорт стандартной формы для создания пользователя в Django
from django.contrib.auth.forms import UserCreationForm
# Импорт модели пользователя, которая расширяет стандартную модель пользователя Django
from users.models import MyUser

# Определение кастомной формы для создания пользователя
class CustomUserCreationForm(UserCreationForm):
    # В этом классе мы переопределяем стандартную форму UserCreationForm
    # и указываем свою модель пользователя и нужные поля.
    class Meta(UserCreationForm.Meta):
        # Указание модели, с которой будет работать форма
        model = MyUser
        # Определение полей, которые будут доступны в форме (кроме стандартных для создания пользователя)
        fields = ('username', 'bio')
