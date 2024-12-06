# Импортирование необходимых модулей из Django
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from blog.models import Post, Comment

# Получение модели пользователя
User = get_user_model()

# Форма для создания и редактирования комментариев
class CommentForm(forms.ModelForm):
    # Указываем, что форма будет работать с моделью Comment, и выбираем поле для использования
    class Meta:
        model = Comment
        fields = ('text',)

# Форма для создания и редактирования постов
class PostForm(forms.ModelForm):
    # Исключаем поле 'author', так как оно будет автоматически заполняться текущим пользователем
    class Meta:
        model = Post
        exclude = ('author',)
        # Настройка виджета для поля 'pub_date', чтобы оно отображалось как дата в форме
        widgets = {'pub_date': forms.DateInput(attrs={'type': 'date'})}

# Кастомная форма регистрации пользователя, расширяющая стандартную форму UserCreationForm
class CustomUserCreationForm(UserCreationForm):
    # Указание модели пользователя и полей, которые будут использоваться в форме
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'bio')

# Форма для редактирования профиля пользователя
class ProfileForm(forms.ModelForm):
    # Указываем модель User и поля для редактирования
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')

# Форма для изменения пароля пользователя
class PasswordChangeForm(forms.Form):
    # Поля для нового пароля и подтверждения пароля
    password1 = forms.CharField(
        label='New password', widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Confirm new password', widget=forms.PasswordInput
    )

    # Проверка на совпадение паролей
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        # Если пароли не совпадают, вызывается ошибка
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
