"""Definition of models."""

from datetime import datetime
from django.db import models
from django.contrib import admin
from django.urls import reverse
from django.contrib.auth.models import User

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

class Blog(models.Model):
    """Модель для статей блога"""
    title = models.CharField(
        max_length=100,
        unique_for_date="posted",
        verbose_name="Заголовок"
    )
    description = models.TextField(verbose_name="Краткое содержание")
    content = models.TextField(verbose_name="Полное содержание")
    posted = models.DateTimeField(
        default=datetime.now,
        db_index=True,
        verbose_name="Дата публикации"
    )
    author = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Автор"
    )
    image = models.ImageField(
        upload_to='app/content/blog_images/',
        default='app/content/blog_default.jpg',
        verbose_name="Изображение статьи",
        help_text="Рекомендуемый размер: 1200x800px"
    )

    def get_absolute_url(self):
        """Возвращает URL для доступа к конкретной записи блога"""
        return reverse("blogpost", args=[str(self.id)])

    def __str__(self):
        """Строковое представление модели"""
        return self.title

    class Meta:
        db_table = "Posts"
        ordering = ["-posted"]
        verbose_name = "статья блога"
        verbose_name_plural = "статьи блога"

class Comment(models.Model):
    """Модель для комментариев к статьям блога"""
    text = models.TextField(verbose_name="Текст комментария")
    date = models.DateTimeField(default=datetime.now, db_index=True, verbose_name="Дата комментария")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор комментария")
    post = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name="Статья комментария")

    def __str__(self):
        return 'Комментарий %s к %s' % (self.author, self.post)

    class Meta:
        db_table = "Comments"
        verbose_name = "комментарий"
        verbose_name_plural = "комментарии"
        ordering = ["date"]

# Регистрация моделей в административном разделе
admin.site.register(Blog)
admin.site.register(Comment)