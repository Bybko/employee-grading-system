# Generated by Django 5.0.8 on 2024-08-28 19:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0007_alter_positions_options_alter_grading_status_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cathedras',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cathedra', models.CharField(max_length=50, verbose_name='Кафедра')),
            ],
            options={
                'verbose_name': 'Кафедры',
                'verbose_name_plural': 'Кафедры',
            },
        ),
        migrations.CreateModel(
            name='Faculties',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('faculty', models.CharField(max_length=50, verbose_name='Факультет')),
            ],
            options={
                'verbose_name': 'Факультеты',
                'verbose_name_plural': 'Факультеты',
            },
        ),
        migrations.RemoveField(
            model_name='profile',
            name='position',
        ),
        migrations.AlterModelOptions(
            name='profile',
            options={'verbose_name': 'Работники', 'verbose_name_plural': 'Работники'},
        ),
        migrations.AddField(
            model_name='profile',
            name='teaching_cathedras',
            field=models.ManyToManyField(blank=True, to='main_app.cathedras', verbose_name='Кафедры'),
        ),
        migrations.AddField(
            model_name='cathedras',
            name='owning_faculty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main_app.faculties', verbose_name='Факультет'),
        ),
        migrations.CreateModel(
            name='Inspectors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('audited_faculty', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main_app.faculties', verbose_name='Факультет')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Юзер')),
            ],
            options={
                'verbose_name': 'Проверяющие',
                'verbose_name_plural': 'Проверяющие',
            },
        ),
        migrations.DeleteModel(
            name='Positions',
        ),
    ]
