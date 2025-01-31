import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "jobsync.app"
    verbose_name = _("Users")

    def ready(self):
        with contextlib.suppress(ImportError):
            import jobsync.app.signals  # noqa: F401
