from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, verbose_name='Юзер', on_delete=models.CASCADE)
    ratings = models.PositiveIntegerField(verbose_name='Рейтинг', default=0)

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинг'

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
        verbose_name = 'Таблицы'
        verbose_name_plural = 'Таблицы'

    def __str__(self):
        return self.table


class Criteria(models.Model):
    title = models.CharField(verbose_name='Наименование работ', max_length=200, blank=False)
    standard_in_points = models.CharField(verbose_name='Норматив в баллах', max_length=30, blank=False)
    table_title = models.ForeignKey(Table, verbose_name='Таблица', on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Нормативы'
        verbose_name_plural = 'Нормативы'

    def __str__(self):
        return self.title


class Grading(models.Model):
    user = models.ForeignKey(User, verbose_name='Юзер', on_delete=models.CASCADE)
    used_standard = models.ForeignKey(Criteria, verbose_name='Норматив', on_delete=models.PROTECT)
    work_done = models.CharField(verbose_name='Выполненная работа', max_length=400, blank=True)
    rating = models.PositiveIntegerField(verbose_name='Баллы', default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'used_standard'], name='unique_user_data')
        ]
        verbose_name = 'Оценивание'
        verbose_name_plural = 'Оценивание'

    # def __str__(self):
    #     return f'{self.user} - {self.used_standard} - {self.rating}'

