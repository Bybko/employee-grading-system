from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


class Faculties(models.Model):
    faculty = models.CharField(verbose_name='Факультет', max_length=50, blank=False)

    class Meta:
        verbose_name = 'Факультеты'
        verbose_name_plural = 'Факультеты'

    def __str__(self):
        return self.faculty


class Cathedras(models.Model):
    cathedra = models.CharField(verbose_name='Кафедра', max_length=50, blank=False)
    owning_faculty = models.ForeignKey(Faculties, verbose_name='Факультет', on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Кафедры'
        verbose_name_plural = 'Кафедры'

    def __str__(self):
        return self.cathedra


class Inspectors(models.Model):
    user = models.OneToOneField(User, verbose_name='Юзер', on_delete=models.CASCADE)
    audited_faculty = models.ForeignKey(Faculties, verbose_name='Факультет', on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Проверяющие'
        verbose_name_plural = 'Проверяющие'

    def __str__(self):
        return self.user.get_full_name()


class Profile(models.Model):
    user = models.OneToOneField(User, verbose_name='Юзер', on_delete=models.CASCADE)
    teaching_cathedras = models.ManyToManyField(Cathedras, verbose_name='Кафедры', blank=True)
    ratings = models.PositiveIntegerField(verbose_name='Рейтинг', default=0)

    class Meta:
        verbose_name = 'Работники'
        verbose_name_plural = 'Работники'

    def __str__(self):
        return self.user.get_full_name()

    def update_ratings(self):
        # Пересчитать рейтинги для пользователя, суммируя только approved записи
        total_points = Grading.objects.filter(
            user=self.user,
            status='approved'
        ).aggregate(total=models.Sum('rating'))['total']
        self.ratings = total_points or 0
        self.save(update_fields=['ratings'])


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
    STATUS_CHOICES = [
        ('not_checked', 'Не проверено'),
        ('approved', 'Одобрено'),
        ('has_errors', 'Есть ошибки'),
    ]
    user = models.ForeignKey(User, verbose_name='Юзер', on_delete=models.CASCADE)
    used_standard = models.ForeignKey(Criteria, verbose_name='Наименование работ', on_delete=models.PROTECT)
    work_done = models.CharField(verbose_name='Выполненная работа', max_length=400, blank=True)
    rating = models.PositiveIntegerField(verbose_name='Баллы', default=0)
    status = models.CharField(
        verbose_name='Статус',
        max_length=20,
        choices=STATUS_CHOICES,
        default='not_checked',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'used_standard'], name='unique_user_data')
        ]
        verbose_name = 'Выполненные работы'
        verbose_name_plural = 'Выполненные работы'

    def __str__(self):
        return f'{self.user} - {self.used_standard} - {self.rating}'


# Сигнал для пересчета рейтинга после сохранения записи в Grading
@receiver(post_save, sender=Grading)
def update_user_profile_on_save(sender, instance, **kwargs):
    instance.user.profile.update_ratings()


# Сигнал для пересчета рейтинга после удаления записи в Grading
@receiver(post_delete, sender=Grading)
def update_user_profile_on_delete(sender, instance, **kwargs):
    instance.user.profile.update_ratings()
