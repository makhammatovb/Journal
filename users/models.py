from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birth_date = models.DateField()
    email = models.EmailField(unique=True)
    organization = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    password_confirmation = models.CharField(max_length=255)
    scientific_degree = models.CharField(max_length=255)
    information = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images', null=True, blank=True)
    can_review = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class PasswordResets(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    reset_code = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'password_resets'
        unique_together = (('user', 'created_at'),)
        index_together = (('user', 'created_at'),)
        verbose_name = 'Password Reset'
        verbose_name_plural = 'Password Resets'
