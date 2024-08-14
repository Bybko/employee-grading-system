from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ratings = models.IntegerField(default=0)


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()


class Table(models.Model):
    table = models.CharField(max_length=50,blank=False)

    def __str__(self):
        return self.table


class Criteria(models.Model):
    title = models.CharField(max_length=200, blank=False)
    standard_in_points = models.CharField(max_length=30, blank=False)
    table_title = models.ForeignKey(Table, on_delete=models.PROTECT)

    def __str__(self):
        return self.title


class Grading(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    used_standard = models.ForeignKey(Criteria, on_delete=models.CASCADE)
    work_done = models.CharField(max_length=400,blank=True)
    rating = models.IntegerField(default=0)

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(fields=['user', 'used_standard'], name='unique_user_data')
    #     ]

    def __str__(self):
        return f'{self.user} - {self.used_standard} - {self.rating}'

