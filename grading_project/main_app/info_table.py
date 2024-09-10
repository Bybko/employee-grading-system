from . import models
from django.contrib.auth.models import User


class Table:
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

    def find_user_grading(self, gradings: list[models.Grading], criterias: list[models.Criteria]) -> None:
        # read how get object by foreign key later
        for grading in gradings:
            if grading.user.user.username == self.user.username:
                for criteria in criterias:
                    if str(criteria.title) == str(grading.used_standard):
                        new_table = Table(grading, criteria)
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

                    gradings = models.Grading.objects.all()
                    criterias = models.Criteria.objects.all()
                    controlled_user_info.find_user_grading(gradings, criterias)

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
