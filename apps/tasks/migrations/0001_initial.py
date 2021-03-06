# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-05 08:13
from __future__ import unicode_literals

import core.utils
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.IntegerField(choices=[(1, 'Pending'), (2, 'Accepted'), (3, 'In Progress'), (4, 'Done')], default=1, verbose_name='Status')),
                ('start_date', models.DateTimeField(verbose_name='Start Date')),
                ('address', models.CharField(max_length=255, verbose_name='Address')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Notes')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='tasks.Category', verbose_name='Category')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to=settings.AUTH_USER_MODEL, verbose_name='Customer')),
                ('tasker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_tasks', to=settings.AUTH_USER_MODEL, verbose_name='Tasker')),
            ],
            options={
                'verbose_name': 'Tasks',
                'verbose_name_plural': 'Tasks',
            },
        ),
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('description', models.TextField(verbose_name='Description')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='todos', to='tasks.Task', verbose_name='Task')),
            ],
            options={
                'verbose_name': 'Todo',
                'verbose_name_plural': 'Todos',
            },
        ),
        migrations.CreateModel(
            name='TodoImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=core.utils.get_images_upload_path, verbose_name='Image')),
                ('todo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='tasks.Todo', verbose_name='Todo')),
            ],
            options={
                'verbose_name': 'Todo Image',
                'verbose_name_plural': 'Todo Images',
            },
        ),
    ]
