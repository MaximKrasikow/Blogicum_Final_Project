from django.utils import timezone
from django.views.generic import (
    CreateView,
    UpdateView,
    DetailView,
)
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import get_user_model
from django.http import Http404
from django.http import HttpResponseForbidden

from blog.forms import PostForm, CommentForm, ProfileForm, PasswordChangeForm
from blog.models import Post, Category, Comment


User = get_user_model()  # Получаем модель пользователя
LIMIT_POSTS = 3  # Лимит на количество постов на странице


def profile_view(request, username):
    # Получаем пользователя по имени
    user = get_object_or_404(User, username=username)
    # Получаем все посты пользователя
    posts = user.posts.all()
    current_time = timezone.now()
    
    # Фильтрация постов для других пользователей (публикуются только те, что опубликованы и в правильной категории)
    if request.user.username != username:
        posts = posts.filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=current_time,
        )

    paginator = Paginator(posts, LIMIT_POSTS)  # Пагинация
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)  # Получаем нужную страницу
    context = {
        "profile": user,
        "page_obj": page_obj,
    }
    return render(request, "blog/profile.html", context)  # Отправляем данные в шаблон


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = "blog/user.html"

    def get_object(self, queryset=None):
        return self.request.user  # Возвращаем текущего пользователя

    def get_success_url(self):
        return reverse_lazy(
            "blog:profile", kwargs={"username": self.request.user.username}
        )  # После успешного обновления редирект на страницу профиля


@login_required
def password_change_view(request, username):
    user = request.user  # Получаем текущего пользователя
    form = PasswordChangeForm(user, request.POST)
    
    # Если запрос POST и форма валидна, сохраняем новый пароль
    if request.method == "POST" and form.is_valid():
        user = form.save()
        update_session_auth_hash(request, user)  # Обновляем сессию, чтобы не сбросить аутентификацию
        return redirect("blog:password_change_done")  # Редирект на страницу "Пароль изменен"
    else:
        form = PasswordChangeForm(user)  # В случае GET возвращаем пустую форму
    
    context = {"form": form}
    return render(request, "blog/password_change_form.html", context)  # Отправляем форму на страницу


class PostMixin:
    model = Post
    form_class = PostForm
    template_name = "blog/create.html"  # Миксин для создания и редактирования постов


class PostCreateView(LoginRequiredMixin, PostMixin, CreateView):
    pk_url_kwarg = "post_id"

    def form_valid(self, form):
        form.instance.author = self.request.user  # Устанавливаем текущего пользователя как автора
        return super().form_valid(form)  # Сохраняем форму


class PostUpdateView(LoginRequiredMixin, PostMixin, UpdateView):
    pk_url_kwarg = "post_id"

    def dispatch(self, request, *args, **kwargs):
        # Проверка, что только автор может редактировать пост
        if self.get_object().author != self.request.user:
            return redirect("blog:post_detail", self.kwargs["post_id"])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_edit"] = True  # Добавляем флаг, что это режим редактирования
        return context


@login_required
def delete_post(request, post_id):
    template_name = "blog/create.html"
    # Получаем пост для удаления только если он принадлежит текущему пользователю
    delete_post = get_object_or_404(Post, pk=post_id, author__username=request.user)
    if request.method != "POST":
        context = {
            "post": delete_post,
            "is_delete": True,  # Флаг для отображения формы удаления
        }
        return render(request, template_name, context)
    # Если запрос POST, удаляем пост
    if delete_post.author == request.user:
        delete_post.delete()
    return redirect("blog:profile", request.user)  # Редирект на страницу профиля


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/detail.html"
    context_object_name = "post"
    pk_url_kwarg = "post_id"

    def get_object(self):
        object = super(PostDetailView, self).get_object()
        # Если пост не опубликован или категория скрыта, выбрасываем ошибку 404
        if self.request.user != object.author and (
            not object.is_published or not object.category.is_published
        ):
            raise Http404()
        return object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()  # Добавляем форму для комментариев
        context["comments"] = self.object.comments.select_related("author")  # Загружаем комментарии с авторами
        return context


def index(request):
    template = "blog/index.html"
    current_time = timezone.now()
    # Фильтруем опубликованные посты с их категориями
    post = Post.objects.select_related("category").filter(
        pub_date__lte=current_time,
        is_published=True,
        category__is_published=True,
    )
    paginator = Paginator(post, LIMIT_POSTS)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)  # Получаем нужную страницу
    context = {"page_obj": page_obj}
    return render(request, template, context)


def category_posts(request, category_slug):
    template = "blog/category.html"
    current_time = timezone.now()
    # Получаем категорию по slug и проверяем, что она опубликована
    category = get_object_or_404(Category, slug=category_slug, is_published=True)
    post_list = category.posts.select_related("category").filter(
        is_published=True,
        pub_date__lte=current_time,
    )
    paginator = Paginator(post_list, LIMIT_POSTS)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)  # Получаем нужную страницу
    context = {"category": category, "page_obj": page_obj}
    return render(request, template, context)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)  # Получаем пост по id
    form = CommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)  # Не сохраняем сразу, чтобы добавить автора и пост
        comment.author = request.user
        comment.post = post
        comment.save()  # Сохраняем комментарий
    return redirect("blog:post_detail", post_id)  # Редирект на страницу поста


@login_required
def edit_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    # Проверяем, что только автор может редактировать комментарий
    if comment.author != request.user:
        return HttpResponseForbidden(
            "У вас нет прав для редактирования этого комментария."
        )

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()  # Сохраняем изменения
            return redirect("blog:post_detail", post_id)
    else:
        form = CommentForm(instance=comment)  # Если GET, то форма для редактирования
    context = {
        "form": form,
        "comment": comment,
        "is_edit": True,  # Флаг редактирования
    }
    return render(request, "blog/comment.html", context)


@login_required
def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    # Проверяем, что только автор может удалить комментарий
    if comment.author != request.user:
        return HttpResponseForbidden("У вас нет прав для удаления этого комментария.")

    if request.method == "POST":
        comment.delete()  # Удаляем комментарий
        return redirect("blog:post_detail", post_id)

    context = {
        "comment": comment,
        "is_delete": True,  # Флаг удаления
    }
    return render(request, "blog/comment.html", context)
