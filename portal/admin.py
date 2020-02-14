from django.contrib import admin
from import_export import resources
from import_export.admin import ExportMixin
from import_export.formats import base_formats

from .forms import QueuerAdminForm
from .models import Building, Queuer


class QueuerResource(resources.ModelResource):
    class Meta:
        model = Queuer


class CustomQueuerAdmin(ExportMixin, admin.ModelAdmin):
    """Admin View for Queuer"""

    resource_class = QueuerResource
    readonly_fields = ("date_applied",)
    list_display = (
        "name",
        "building_applied",
        "current_waitlist",
        "all_verified",
        "placed",
        "contact_number",
        "email",
        "marriage_certificate",
    )
    list_filter = (
        "building_applied",
        "placed",
    )
    search_fields = ("name", "contact_number")
    # fieldsets = (
    #     (None, {'fields': ["building_applied", "placed", "room_number", ]}),

    #     ("Personal Info", {
    #         'fields': ["name",
    #                    "contact_number",
    #                    "email", ]
    #     }),

    #     ("Certificates", {
    #         'fields': ["marriage_certificate"]
    #     })
    # )
    form = QueuerAdminForm

    def get_export_formats(self):
        formats = (
            base_formats.XLS,
            base_formats.XLSX,
            base_formats.CSV,
            base_formats.HTML,
        )

        return [f for f in formats if f().can_export()]

    def Mark_as_placed(modeladmin, news, queryset):
        queryset.update(placed=True)

    def Mark_as_not_placed(modeladmin, news, queryset):
        queryset.update(placed=False)

    actions = [
        Mark_as_placed,
        Mark_as_not_placed,
    ]


# No one can change users or groups.
# admin.site.unregister(User)
# admin.site.unregister(Group)

# Register your models here.
admin.site.register(Building)
admin.site.register(Queuer, CustomQueuerAdmin)
