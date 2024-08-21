from . import models
from django.contrib.auth.models import User


class Table:
    def __init__(self, grading: models.Grading, criteria: models.Criteria):
        self.grading = grading
        self.criteria = criteria


class InfoTable:
    def __init__(self, user: User):
        self.user = user
        self.user_tables = []

    def find_user_grading(self, gradings: list[models.Grading], criterias: list[models.Criteria]) -> None:
        # read how get object by foreign key later
        for grading in gradings:
            if grading.user.username == self.user.username:
                for criteria in criterias:
                    if str(criteria.title) == str(grading.used_standard):
                        new_table = Table(grading, criteria)
                        self.user_tables.append(new_table)
