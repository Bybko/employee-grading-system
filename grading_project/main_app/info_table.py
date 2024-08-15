from . import models
from django.contrib.auth.models import User


class InfoTable:
    def __init__(self, user: User):
        self.user = user
        self.user_gradings = []

    def find_user_grading(self, gradings: list[models.Grading]) -> None:
        for grading in gradings:
            if grading.user.username == self.user.username:
                self.user_gradings.append(grading)
