from . import models
from django.contrib.auth.models import User


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

    def sort_all_self_gradins(self,  sort_field: str) -> None:
        profile = models.Profile.objects.get(user=self.user)
        self.sorted_gradings = (models.Grading.objects.filter(user=profile).
                                                    order_by(sort_field).distinct())

    def sort_all_controlled_gradings(self, sort_field: str) -> None:
        teacher_profiles = [teacher_info.user.profile for teacher_info in self.controlled_users]

        self.sorted_controlled_teachers_gradings = (models.Grading.objects.filter(user__in=teacher_profiles).
                                                    order_by(sort_field).distinct())
