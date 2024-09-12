from . import models
from django.contrib.auth.models import User


class Table:
    # нужен ли вообще этот класс если из одного можно получить другое? в том числе в html
    def __init__(self, grading: models.Grading, criteria: models.Criteria):
        self.grading = grading
        self.criteria = criteria


class InfoTable:
    def __init__(self, user: User):
        self.user = user
        self.user_role = 'None'
        self.cathedras = []
        self.faculties = []
        self.user_tables = []
        self.controlled_users = []
        self.controlled_cathedras_users = {}
        self.controlled_faculties = []
        self.sorted_controlled_teachers_gradings = []

    def find_user_grading(self, gradings: list[models.Grading]) -> None:
        for grading in gradings:
            if grading.user.user.username == self.user.username:
                new_table = Table(grading, grading.used_standard)
                self.user_tables.append(new_table)

    def set_faculties(self, user_object: User) -> None:
        faculties = models.Inspectors.objects.get(user=user_object).audited_faculty

        for faculty in faculties.all():
            self.controlled_faculties.append(faculty.faculty)

    def find_controlled_users(self, profiles: list[models.Profile]) -> None:
        for profile in profiles:
            for teaching_cathedra in profile.teaching_cathedras.all():
                compared_cathedra = models.Cathedras.objects.get(cathedra=teaching_cathedra)

                if compared_cathedra.owning_faculty.faculty in self.controlled_faculties:
                    controlled_user_info = InfoTable(profile.user)
                    controlled_user_info.cathedras = profile.teaching_cathedras
                    for cathedra in controlled_user_info.cathedras.all():
                        if cathedra.owning_faculty.faculty not in controlled_user_info.faculties:
                            controlled_user_info.faculties.append(cathedra.owning_faculty.faculty)

                    controlled_user_info.user_role = 'Worker'

                    gradings = models.Grading.objects.all() # change to filter by user and delete method bellow
                    controlled_user_info.find_user_grading(gradings)

                    self.controlled_users.append(controlled_user_info)
                    break

        self.sort_users_by_cathedras()

    def sort_users_by_cathedras(self) -> None:
        cathedras = []
        for faculty in self.controlled_faculties:
            faculty_cathedras = models.Cathedras.objects.filter(owning_faculty=
                                                        models.Faculties.objects.get(faculty=faculty))
            cathedras.extend(faculty_cathedras)

        for cathedra in cathedras:
            if cathedra not in self.controlled_cathedras_users:
                self.controlled_cathedras_users[cathedra] = []

            for teacher in self.controlled_users:
                if cathedra in teacher.cathedras.all():
                    self.controlled_cathedras_users[cathedra].append(teacher)

    def sort_all_teachers_gradings(self, sort_field: str) -> None:
        # а зачем тогда другие формируемые списки, если по сути вот здесь самое главное? надо изучить
        teacher_profiles = [teacher_info.user.profile for teacher_info in self.controlled_users]

        self.sorted_controlled_teachers_gradings = (models.Grading.objects.filter(user__in=teacher_profiles).
                                                    order_by(sort_field).distinct())
