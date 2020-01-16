from django.contrib import admin
from django.contrib.auth.models import Group, User

from .forms import QueuerAdminForm
from .models import Building, Queuer


class CustomQueuerAdmin(admin.ModelAdmin):
    """Admin View for Queuer"""

    list_display = (
        "name",
        "building_applied",
        "current_waitlist",
        "placed",
        "contact_number",
        "email",
    )
    list_filter = ("building_applied", "placed")
    search_fields = ("name", "contact_number")
    form = QueuerAdminForm

    def Mark_as_placed(modeladmin, news, queryset):
        queryset.update(placed=True)

    def Mark_as_not_placed(modeladmin, news, queryset):
        queryset.update(placed=False)

    actions = [
        Mark_as_placed,
        Mark_as_not_placed,
    ]


# No one can change users or groups.
admin.site.unregister(User)
admin.site.unregister(Group)

# Register your models here.
admin.site.register(Building)
admin.site.register(Queuer, CustomQueuerAdmin)
