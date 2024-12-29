from django.db import models
from django.contrib.auth.models import AbstractUser



CHOICES = {
    'Opened': 'Opened',
    'Closed': 'Closed'
}

class Pool(models.Model):
    """Описывает бассейны."""
    name = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='Читаемая ссылка')
    adress = models.TextField(max_length=200, verbose_name='Адрес')
    capacity_left = models.IntegerField(default=0)
    max_capacity = models.IntegerField(default=0)
    timetable = models.CharField()
    status = models.CharField(verbose_name='Статус', max_length=15, choices=CHOICES, default='open')

    class Meta:
        verbose_name = 'Бассейн'
        verbose_name_plural = 'Бассейны'
        ordering = ['id']

CHOICES2 = {
    'User': 'User',
    'Admin': 'Admin',
}

class CustomUser(AbstractUser):
    """Описывает пользователя."""
    role = models.CharField(
        verbose_name='Роль', max_length=15, choices=CHOICES2, default='user'
        )

    username = models.CharField(
        verbose_name='Выбранное имя', max_length=150, unique=True, blank=False
    )

    login = models.CharField(verbose_name='Почта', blank=False)
    password = models.CharField(verbose_name='Пароль', blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'], name='unique_username_email'
                ),
        ]




class Booking(models.Model):
     """Описывает связь бассейнов и пользователей."""
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False)  # Связь с пользователем
	pool = models.ForeignKey(Pool, on_delete=models.CASCADE, null=False)  # Связь с бассейном

	def __str__(self):
		return f"{self.user.username} booked {self.pool.name}"
