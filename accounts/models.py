from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

class CustomUser(AbstractUser):

    email = models.EmailField(unique=True, verbose_name='Email адрес')

    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Номер телефона должен быть в формате: '+999999999'. До 15 цифр."
    )
    
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17,
        blank=True,
        verbose_name='Номер телефона'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        db_table = 'custom_users'

    def __str__(self):
        return self.email

class UserProfile(models.Model):
    
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='profile'
    )
 
    location = models.CharField(
        max_length=30,
        blank=True,
        verbose_name='Местоположение'
    )

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'
        db_table = 'user_profiles'

    def __str__(self):
        return f'Профиль {self.user.email}'   