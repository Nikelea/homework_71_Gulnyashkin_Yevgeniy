# Generated by Django 4.0.10 on 2023-04-20 09:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Sex',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=10, verbose_name='Пол')),
            ],
            options={
                'verbose_name': 'Пол',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(upload_to='user_pics', verbose_name='Аватар')),
                ('about', models.TextField(blank=True, max_length=2000, verbose_name='О себе')),
                ('phone', models.IntegerField(blank=True, null=True, verbose_name='Номер телефона')),
                ('publications_counter', models.IntegerField(default=0, null=True, verbose_name='Число публикаций')),
                ('subscriptions_counter', models.IntegerField(default=0, null=True, verbose_name='Число подписок')),
                ('subscribers_counter', models.IntegerField(default=0, null=True, verbose_name='Число подписчиков')),
                ('sex', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='profiles', to='accounts.sex')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Профиль',
                'verbose_name_plural': 'Профили',
            },
        ),
        migrations.CreateModel(
            name='Follower',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время подписи')),
                ('follow', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='follower', to=settings.AUTH_USER_MODEL, verbose_name='Последователь')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscribers', to=settings.AUTH_USER_MODEL, verbose_name='Лидер')),
            ],
        ),
    ]
