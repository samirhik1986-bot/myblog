from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.CharField(verbose_name="Текст поста")
    date_posted = models.DateTimeField(default=timezone.now, verbose_name="Дата публикации")
    image = models.ImageField(upload_to="post_images/", blank=True, null=True, verbose_name="Картинка")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор", null=True)
def __str__(self):
    return self.title
def get_absolute_url(self):
    return reverse("post-detail", kwargs={"pk": self.pk})
class Meta:
    verbose_name = 'Запись блога'
    verbose_name_plural = 'Записи блога'
    ordering = ['-date-posted']
