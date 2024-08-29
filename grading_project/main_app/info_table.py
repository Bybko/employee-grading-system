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
        self.user_tables = []
        self.controlled_users = []
        self.controlled_faculty = None

    def find_user_grading(self, gradings: list[models.Grading], criterias: list[models.Criteria]) -> None:
        # read how get object by foreign key later
        for grading in gradings:
            if grading.user.username == self.user.username:
                for criteria in criterias:
                    if str(criteria.title) == str(grading.used_standard):
                        new_table = Table(grading, criteria)
                        self.user_tables.append(new_table)

    def set_faculty(self, faculty: models.Faculties):
        self.controlled_faculty = faculty.faculty

    def find_controlled_users(self, profiles: list[models.Profile]) -> None:
        for profile in profiles:
            for teaching_cathedra in profile.teaching_cathedras.all():
                compared_cathedra = models.Cathedras.objects.get(cathedra=teaching_cathedra)
                if compared_cathedra.owning_faculty.faculty == self.controlled_faculty:
                    controlled_user_info = InfoTable(profile.user)
                    controlled_user_info.cathedras = profile.teaching_cathedras
                    controlled_user_info.user_role = 'Worker'

                    gradings = models.Grading.objects.all()
                    criterias = models.Criteria.objects.all()
                    controlled_user_info.find_user_grading(gradings, criterias)

                    self.controlled_users.append(controlled_user_info)
                    break
