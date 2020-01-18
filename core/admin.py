from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from core.models import UserProfile


class UserProfileInline(admin.StackedInline):
    """ Define an inline admin descriptor for User Profile which acts a bit like a singleton """

    model = UserProfile
    can_delete = False
    verbose_name = "User Profile"
    verbose_name_plural = "User Profiles"


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    # TODO: Move Userprofile section below personal info
    inlines = (UserProfileInline,)
    # Add proxy(User profile) on admin page
    list_display = (
        "username",
        "email",
        "is_staff",
    )


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
