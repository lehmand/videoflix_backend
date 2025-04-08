# Generated by Django 5.2 on 2025-04-08 19:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Videos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.TextField(max_length=150)),
                ('description', models.CharField(blank=True, max_length=1000)),
                ('file', models.FileField(upload_to='videos')),
                ('thumbnail', models.FileField(upload_to='thumbnails')),
                ('genre', models.CharField(blank=True, max_length=150)),
            ],
        ),
    ]
