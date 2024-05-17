from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MembershipsConfig(AppConfig):
    name = "my_awesome_project.memberships"
    verbose_name = _("Memberships")
