from django.db import models
from django_lifecycle import LifecycleModelMixin

from my_awesome_project.users.models import User
from my_awesome_project.utils.common import get_short_uuid
from my_awesome_project.utils.models import BaseModel


class Organization(LifecycleModelMixin, BaseModel):
    name = models.CharField(max_length=256, unique=True)
    description = models.TextField(max_length=256, blank=True)
    uuid = models.CharField(
        max_length=12,
        unique=True,
        editable=False,
        default=get_short_uuid,
    )

    def __str__(self):
        return self.name


class Membership(LifecycleModelMixin, BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    uuid = models.CharField(
        max_length=12,
        unique=True,
        editable=False,
        default=get_short_uuid,
    )

    def __str__(self):
        return f"{self.user.email}"

    def is_email_verified(self):
        return any(
            email
            for email in self.user.emailaddress_set.all()
            if email.verified and email.email == self.user.email
        )

    def verify_email(self):
        pass
