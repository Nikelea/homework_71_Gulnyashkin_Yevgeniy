from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver


class Sex(models.Model):
    title = models.CharField(max_length=10, verbose_name='Пол')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пол'


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), related_name='profile', on_delete=models.CASCADE,
                                verbose_name='Пользователь')
    avatar = models.ImageField(blank=False, upload_to='user_pics', verbose_name='Аватар')
    about = models.TextField(max_length=2000, blank=True, verbose_name='О себе')
    phone = models.IntegerField(null=True, blank=True, verbose_name='Номер телефона')
    sex = models.ForeignKey(Sex, on_delete=models.SET_NULL, null=True, blank=True, related_name='profiles')
    publications_counter = models.IntegerField(null=True, blank=False, default=0, verbose_name='Число публикаций')
    subscriptions_counter = models.IntegerField(null=True, blank=False, default=0, verbose_name='Число подписок')
    subscribers_counter = models.IntegerField(null=True, blank=False, default=0, verbose_name='Число подписчиков')

    def __str__(self):
        return self.user.username + self.user.get_full_name() + "'s Profile"

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

class Follower(models.Model):
    user = models.ForeignKey(get_user_model(), related_name='subscribers', on_delete=models.CASCADE, verbose_name='Лидер')
    follow = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='follower', 
        verbose_name='Последователь',
        blank=True
        )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время подписи')

    def __str__(self):
        return "{}".format(self.follow) 

