from django.urls import path, re_path
from blog import views

app_name = 'blog'


urlpatterns = [
    # Главная страница (список всех постов)
    path('', views.index, name='index'),

    # Страница с постами по категории
    path(
        'category/<slug:category_slug>/',
        views.category_posts,
        name='category_posts',
    ),

    # Профиль пользователя
    path('profile/<username>/', views.profile_view, name='profile'),

    # Страница редактирования профиля (разрешены символы в username, включая кириллицу)
    re_path(r'^profile/(?P<username>[\w-]+)/edit_profile/$', views.ProfileUpdateView.as_view(), name='edit_profile'),

    # Страница для создания поста
    path('posts/create/', views.PostCreateView.as_view(), name='create_post'),

    # Страница детального просмотра поста
    path(
        'posts/<int:post_id>/',
        views.PostDetailView.as_view(),
        name='post_detail',
    ),

    # Страница для редактирования поста
    path(
        'posts/<int:post_id>/edit/',
        views.PostUpdateView.as_view(),
        name='edit_post',
    ),

    # Страница для удаления поста
    path('posts/<int:post_id>/delete/', views.delete_post, name='delete_post'),

    # Страница для добавления комментария к посту
    path('posts/<int:post_id>/comment', views.add_comment, name='add_comment'),

    # Страница для редактирования комментария
    path(
        'posts/<int:post_id>/edit_comment/<int:comment_id>/',
        views.edit_comment,
        name='edit_comment',
    ),

    # Страница для удаления комментария
    path(
        'posts/<int:post_id>/delete_comment/<int:comment_id>/',
        views.delete_comment,
        name='delete_comment',
    ),
]
