from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from .constants import LIMITATION, TITLE_LENGHT

User = get_user_model()


class CommonInfoModel(models.Model):
    """Абстрактная модель для хранения общей информации"""

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Добавлено"
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name="Опубликовано",
        help_text="Снимите галочку, чтобы скрыть публикацию.",
    )

    class Meta:
        abstract = True
        verbose_name = "Общая информация"


class Category(CommonInfoModel):
    """Модель для категорий"""

    title = models.CharField(max_length=TITLE_LENGHT, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание")
    slug = models.SlugField(
        unique=True,
        verbose_name="Идентификатор",
        help_text=(
            "Идентификатор страницы для URL; "
            "разрешены символы латиницы, цифры, дефис и подчёркивание."
        ),
    )

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.title[:LIMITATION]


class Location(CommonInfoModel):
    """Модель для местоположений"""

    name = models.CharField(
        max_length=TITLE_LENGHT, verbose_name="Название места"
    )

    class Meta:
        verbose_name = "местоположение"
        verbose_name_plural = "Местоположения"

    def __str__(self):
        return self.name[:LIMITATION]


class Post(CommonInfoModel):
    """Модель для постов"""

    title = models.CharField(max_length=TITLE_LENGHT, verbose_name="Заголовок")
    text = models.TextField(verbose_name="Текст")
    is_scheduled = models.BooleanField(default=False)
    pub_date = models.DateTimeField(
        verbose_name="Дата и время публикации",
        help_text=(
            "Если установить дату и время в будущем — "
            "можно делать отложенные публикации."
        ),
        default=timezone.now,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор публикации",
        related_name="posts",
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Местоположение",
        related_name="posts",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Категория",
        related_name="posts",
    )
    image = models.ImageField(
        upload_to="post_images/",
        blank=True,
        null=True,
        verbose_name="Изображение"
    )

    class Meta:
        verbose_name = "публикация"
        verbose_name_plural = "Публикации"
        ordering = ["-pub_date"]

    def __str__(self):
        return self.title[:LIMITATION]


class Comment(models.Model):
    """Модель для комментариев"""

    text = models.TextField("Текст комментария")
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Пост"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Добавлено"
    )

    class Meta:
        ordering = ["created_at"]
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return self.text[:LIMITATION]
