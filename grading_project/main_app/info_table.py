from . import models
from django.contrib.auth.models import User
from django.db.models import Case, When, IntegerField


class InfoTable:
    def __init__(self, user: User):
        self.user = user
        self.user_role = 'None'
        self.faculties = []
        self.controlled_faculties = []
        self.sorted_gradings = []
        self.sorted_controlled_teachers_gradings = []
        self.controlled_users = []

    def set_controlled_faculties(self) -> None:
        faculties = models.Inspectors.objects.get(user=self.user).audited_faculty

        for faculty in faculties.all():
            self.controlled_faculties.append(faculty.faculty)

    def find_controlled_users(self) -> None:
        profiles = models.Profile.objects.all()

        for profile in profiles:
            for teaching_cathedra in profile.teaching_cathedras.all():
                compared_cathedra = models.Cathedras.objects.get(cathedra=teaching_cathedra)

                if compared_cathedra.owning_faculty.faculty in self.controlled_faculties:
                    controlled_user_info = InfoTable(profile.user)
                    for cathedra in controlled_user_info.user.profile.teaching_cathedras.all():
                        if cathedra.owning_faculty.faculty not in controlled_user_info.faculties:
                            controlled_user_info.faculties.append(cathedra.owning_faculty.faculty)

                    controlled_user_info.user_role = 'Teacher'
                    self.controlled_users.append(controlled_user_info)
                    break

    def sort_all_self_gradins(self,  sort_field: str, order_stage: int = 1) -> None:
        if sort_field == 'status' or sort_field == '-status':
            profile = models.Profile.objects.get(user=self.user)
            self.sorted_gradings = (
                models.Grading.objects.filter(user=profile)
                .annotate(status_order=self.set_status_order(order_stage))
                .order_by('status_order')
            )
        else:
            profile = models.Profile.objects.get(user=self.user)
            self.sorted_gradings = (models.Grading.objects.filter(user=profile).
                                                        order_by(sort_field).distinct())

    def sort_all_controlled_gradings(self, sort_field: str, order_stage: int = 1) -> None:
        teacher_profiles = [teacher_info.user.profile for teacher_info in self.controlled_users]
        if sort_field == 'status' or sort_field == '-status':
            self.sorted_controlled_teachers_gradings = (
                models.Grading.objects.filter(user__in=teacher_profiles)
                .annotate(status_order=self.set_status_order(order_stage))
                .order_by('status_order')
            )
        else:
            self.sorted_controlled_teachers_gradings = (models.Grading.objects.
                                                        filter(user__in=teacher_profiles).
                                                        order_by(sort_field).distinct())

    def set_status_order(self, order_stage: int) -> Case:
        # Manage status sorting priorities depending on order_stage
        if order_stage == 1:
            status_order = Case(
                When(status='approved', then=1),
                When(status='has_errors', then=2),
                When(status='not_checked', then=3),
                output_field=IntegerField()
            )
        elif order_stage == 2:
            status_order = Case(
                When(status='has_errors', then=1),
                When(status='approved', then=2),
                When(status='not_checked', then=3),
                output_field=IntegerField()
            )
        else:
            status_order = Case(
                When(status='not_checked', then=1),
                When(status='has_errors', then=2),
                When(status='approved', then=3),
                output_field=IntegerField()
            )

        return status_order
