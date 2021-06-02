# Generated by Django 3.0.5 on 2021-04-26 07:16

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
            name='NotificationHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(blank=True, default='')),
                ('content', models.TextField(blank=True, default='')),
                ('status', models.CharField(choices=[('N', 'New'), ('R', 'Read'), ('U', 'Unread')], default='N', max_length=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_read', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(blank=True, max_length=255, unique=True)),
                ('to_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'notification_histories',
            },
        ),
        migrations.CreateModel(
            name='NotificationCount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'notification_counts',
            },
        ),
    ]
