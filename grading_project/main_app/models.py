from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


class Positions(models.Model):
    position_name = models.CharField(verbose_name='Должность', max_length=50, blank=False)

    class Meta:
        verbose_name = 'Должности'
        verbose_name_plural = 'Должности'

    def __str__(self):
        return self.position_name


class Profile(models.Model):
    user = models.OneToOneField(User, verbose_name='Юзер', on_delete=models.CASCADE)
    position = models.ForeignKey(Positions, verbose_name='Должность', on_delete=models.PROTECT, null=True, blank=True)
    ratings = models.PositiveIntegerField(verbose_name='Рейтинг', default=0)

    class Meta:
        verbose_name = 'Рейтинг работников'
        verbose_name_plural = 'Рейтинг работников'

    def __str__(self):
        return f'{self.user.get_full_name()}, Баллы: {self.ratings}'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()


class Table(models.Model):
    table = models.CharField(verbose_name='Название таблицы', max_length=50, blank=False)

    class Meta:
        verbose_name = 'Названия таблиц'
        verbose_name_plural = 'Названия таблиц'

    def __str__(self):
        return self.table


class Criteria(models.Model):
    title = models.CharField(verbose_name='Наименование работ', max_length=200, blank=False)
    standard_in_points = models.CharField(verbose_name='Норматив в баллах', max_length=30, blank=False)
    table_title = models.ForeignKey(Table, verbose_name='Таблица', on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
        verbose_name = 'Работы и нормативы'
        verbose_name_plural = 'Работы и нормативы'

    def __str__(self):
        return self.title


class Grading(models.Model):
    user = models.ForeignKey(User, verbose_name='Юзер', on_delete=models.CASCADE)
    used_standard = models.ForeignKey(Criteria, verbose_name='Наименование работ', on_delete=models.PROTECT)
    work_done = models.CharField(verbose_name='Выполненная работа', max_length=400, blank=True)
    rating = models.PositiveIntegerField(verbose_name='Баллы', default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'used_standard'], name='unique_user_data')
        ]
        verbose_name = 'Выполненные работы'
        verbose_name_plural = 'Выполненные работы'

    def __str__(self):
        return f'{self.user} - {self.used_standard} - {self.rating}'

# Сигнал для обновления баллов в Profile после сохранения Grading


@receiver(post_save, sender=Grading)
def update_user_profile_on_save(sender, instance, **kwargs):
    user_profile = instance.user.profile
    total_points = Grading.objects.filter(user=instance.user).aggregate(total=models.Sum('rating'))['total']
    user_profile.ratings = total_points or 0
    user_profile.save()

# Сигнал для обновления баллов в Profile после удаления Grading


@receiver(post_delete, sender=Grading)
def update_user_profile_on_delete(sender, instance, **kwargs):
    user_profile = instance.user.profile
    total_points = Grading.objects.filter(user=instance.user).aggregate(total=models.Sum('rating'))['total']
    user_profile.ratings = total_points or 0
    user_profile.save()