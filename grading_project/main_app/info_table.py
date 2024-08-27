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
        self.user_tables = []
        self.controlled_users = []

    def find_user_grading(self, gradings: list[models.Grading], criterias: list[models.Criteria]) -> None:
        # read how get object by foreign key later
        for grading in gradings:
            if grading.user.username == self.user.username:
                for criteria in criterias:
                    if str(criteria.title) == str(grading.used_standard):
                        new_table = Table(grading, criteria)
                        self.user_tables.append(new_table)

    def set_role(self, profile: models.Profile) -> None:
        self.user_role = profile.position.position_name

    def find_controlled_users(self, users: list[User]) -> None:
        for user_object in users:
            role = models.Profile.objects.get(user=user_object)

            if role.position.position_name == 'Работник':
                info = InfoTable(user_object)
                info.set_role(role)

                gradings = models.Grading.objects.all()
                criterias = models.Criteria.objects.all()
                info.find_user_grading(gradings, criterias)

                self.controlled_users.append(info)
