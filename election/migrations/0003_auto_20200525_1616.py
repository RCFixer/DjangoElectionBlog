# Generated by Django 2.2 on 2020-05-25 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20200523_1627'),
        ('election', '0002_auto_20200525_1541'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='survey',
            name='post',
        ),
        migrations.AddField(
            model_name='survey',
            name='posts',
            field=models.ManyToManyField(blank=True, related_name='surveys', to='blog.Post'),
        ),
    ]