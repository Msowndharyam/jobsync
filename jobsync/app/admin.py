from allauth.account.decorators import secure_admin_login
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.utils.translation import gettext_lazy as _

from .forms import UserAdminChangeForm
from .forms import UserAdminCreationForm
from .models import User

if settings.DJANGO_ADMIN_FORCE_ALLAUTH:
    # Force the `admin` sign in process to go through the `django-allauth` workflow:
    # https://docs.allauth.org/en/latest/common/admin.html#admin
    admin.autodiscover()
    admin.site.login = secure_admin_login(admin.site.login)  # type: ignore[method-assign]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    list_display = ['email', 'name', 'role', 'is_active', 'is_staff']
    search_fields = ['email', 'name']
    ordering = ['id']
    fieldsets = (
        (None, {'fields': ('email', 'password', 'name', 'role', 'job_title', 'location', 'organisation')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
       
    )

from django.contrib import admin
from .models import User, JobListing, JobApplication, Skill

# Register your models here.
# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('email', 'name', 'role', 'is_active', 'is_staff')
#     search_fields = ('email', 'name')
#     list_filter = ('role', 'is_active', 'is_staff')

@admin.register(JobListing)
class JobListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'location', 'posted_at',]
    search_fields = ['title', 'company']
    list_filter = ['location']
    fieldsets = (
        (None, {'fields': ( 'title', 'company', 'location', 'description', 'required_skills', 'external_url', 'posted_at')}),
    )

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['job','applicant','applied_date' ]
    search_fields = ['user__email', 'job__title']
    list_filter = ['applied_date']
    fieldsets = (
        (None, {'fields': ('user', 'job', 'cover_letter', 'applied_at')}),
    )

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    fieldsets = (
        (None, {'fields': ('name',)}),
    )
