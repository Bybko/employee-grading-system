# Generated by Django 5.0.8 on 2024-09-24 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0010_alter_grading_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grading',
            name='rating',
            field=models.FloatField(default=0.0, verbose_name='Баллы'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='ratings',
            field=models.FloatField(default=0.0, verbose_name='Рейтинг'),
        ),
    ]
