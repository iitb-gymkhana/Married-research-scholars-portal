from django.contrib import admin
from import_export import resources
from import_export.admin import ExportMixin
from import_export.formats import base_formats
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html
from .models import Applicant, Waitlist, OccupiedList, VacatedList
from django.utils.translation import gettext_lazy as _
from .forms import OccupiedListForm, VacatedListForm, MailingListForm
from django.db.models import Q

class OccupiedFilter(admin.SimpleListFilter):
    title = _('Building Occupied')
    parameter_name = 'occupiedlist__id'

    def lookups(self, request, model_admin):
        return (
            ('2', _('Tulsi')),
            ('3', _('Manas')),
            ('1', _('Type-1')),
        )

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.filter(occupiedlist__id=1)
        if self.value() == '2':
            return queryset.filter(occupiedlist__id=2)
        if self.value() == '3':
            return queryset.filter(occupiedlist__id=3)

class VacatedFilter(admin.SimpleListFilter):
    title = _('Building Vacated')
    parameter_name = 'vacatedlist__id'
    def lookups(self, request, model_admin):
        return (
            ('2', _('Tulsi')),
            ('3', _('Manas')),
            ('1', _('Type-1')),
        )

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.filter(vacatedlist__id=1)
        if self.value() == '2':
            return queryset.filter(vacatedlist__id=2)
        if self.value() == '3':
            return queryset.filter(vacatedlist__id=3)


class ApplicantResource(resources.ModelResource):
    class Meta:
        model = Applicant


class HCUAdminSite(admin.AdminSite):
    site_header = "HCU Admin"
    site_title = "HCU Admin Portal"
    index_title = "Welcome to the HCU Admin Portal"

class HCUAdminApplicantResource(resources.ModelResource):
    class Meta:
        model = Applicant

class HCUAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = HCUAdminApplicantResource
    list_display = (
        'name',
        'roll_number',
        'email',
        'department',
        "waitlist_Type1",
        "waitlist_Tulsi",
        "waitlist_MRSB",
        "all_verified",
        "occupied_Type1",
        "occupied_Tulsi",
        "occupied_MRSB"
    )

    search_fields = ("name", "roll_number")
    list_filter = (
        OccupiedFilter,
        VacatedFilter
    )
    readonly_fields = ('name', 'roll_number', 'date_of_registration', 'department',
                       'email', 'phone_number', 'permanent_address', 'scholarship', 'date_of_scholarship', 'course_work_completed_on',
                       'course_work_completed_by', 'scholarship_awarded_upto', 'acad_details_verified', 'acad_details_verification_date', 'marriage_certificate', 'joint_photograph_with_spouse',
                       'coursework_grade_sheet', 'recommendation_of_guide_for_accomodation', 'spouse_name', 'spouse_roll_number', 'spouse_designation', 'application_received_by_hcu_date')
    exclude = ['acad_details_verification_date']
    fields = ('name', 'roll_number', 'date_of_registration', 'department', 'email', 'phone_number', 'permanent_address', 'scholarship',
              'date_of_scholarship', 'course_work_completed_on', 'course_work_completed_by', 'marriage_certificate', 'joint_photograph_with_spouse',
              'coursework_grade_sheet', 'recommendation_of_guide_for_accomodation', 'spouse_name', 'spouse_roll_number', 'spouse_designation',
              'marriage_certificate_verified', 'joint_photograph_with_spouse_verified', 'coursework_grade_sheet_verified', 'recommendation_of_guide_for_accomodation_verified',
              'feedback', 'application_received_by_hcu_date', 'verified_time')

    def get_queryset(self, request):
        qs = super(HCUAdmin, self).get_queryset(request)
        
        return qs.filter(acad_details_verified=True).order_by('acad_details_verification_date',
                                                              'waitlist_Type1', 'waitlist_Tulsi',
                                                              'waitlist_MRSB')

    def get_export_formats(self):
        formats = (
            base_formats.XLS,
            base_formats.XLSX,
            base_formats.CSV,
            base_formats.HTML,
        )

        return [f for f in formats if f().can_export()]

class AcadAdminSite(admin.AdminSite):
    site_header = "Academic Section"
    site_title = "Academic Section Admin Portal"
    index_title = "Welcome to the Academic Section Admin Portal"

class AcadAdminApplicantResource(resources.ModelResource):
    class Meta:
        model = Applicant
        # fields = ('name', 'roll_number', 'date_of_registration', 'department',
        # 'email', 'phone_number', 'permanent_address', 'scholarship', 'course_work_completed_on',
        # 'course_work_completed_by')
class AcadAdmin(admin.ModelAdmin):
    resource_class = AcadAdminApplicantResource
    list_display = (
        'name',
        'roll_number',
        'department',
        'acad_details_verified'
    )
    fields = ('name', 'roll_number', 'date_of_registration', 'department',
              'email', 'phone_number', 'permanent_address', 'scholarship', 'date_of_scholarship', 'course_work_completed_on','date_applied',
              'course_work_completed_by', 'scholarship_awarded_upto', 'acad_details_verified', 'acad_details_verification_date', 'acadsection_feedback')
    readonly_fields = ('name', 'roll_number', 'date_of_registration', 'department',
                       'email', 'phone_number', 'permanent_address', 'scholarship', 'date_of_scholarship', 'course_work_completed_on',
                       'course_work_completed_by', 'date_applied')

    def get_queryset(self, request):
        qs = super(AcadAdmin, self).get_queryset(request)

        return qs.order_by('date_applied')

class ApplicantAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = ApplicantResource
    list_display = (
        'name',
        'roll_number',
        'email',
        'department',
        "waitlist_Type1",
        "waitlist_Tulsi",
        "waitlist_MRSB",
        "all_verified",
        "occupied_Type1",
        "occupied_Tulsi",
        "occupied_MRSB"
    )

    search_fields = ("name", "roll_number")
    list_filter = (
        OccupiedFilter,
        VacatedFilter,
    )

    def get_export_formats(self):
        formats = (
            base_formats.XLS,
            base_formats.XLSX,
            base_formats.CSV,
            base_formats.HTML,
        )

        return [f for f in formats if f().can_export()]

# class CustomQueuerAdmin(ExportMixin, admin.ModelAdmin):
#     """Admin View for Queuer"""

#     resource_class = QueuerResource
#     readonly_fields = ("date_applied",)
#     list_display = (
#         "name",
#         # "building_applied",
#         "waitlist_Type1",
#         "waitlist_Tulsi",
#         "waitlist_MRSB",
#         "all_verified",
#         "placed",
#         "contact_number",
#         "email",
#         # "marriage_certificate",
#     )
#     list_filter = (
#         "building",
#         # "tulsi",
#         # "mrsb",
#         # "type1",
#         "placed",
#     )
#     search_fields = ("name", "contact_number")
#     # fieldsets = (
#     #     (None, {'fields': ["building_applied", "placed", "room_number", ]}),

#     #     ("Personal Info", {
#     #         'fields': ["name",
#     #                    "contact_number",
#     #                    "email", ]
#     #     }),

#     #     ("Certificates", {
#     #         'fields': ["marriage_certificate"]
#     #     })
#     # )
#     form = QueuerAdminForm

#     def get_export_formats(self):
#         formats = (
#             base_formats.XLS,
#             base_formats.XLSX,
#             base_formats.CSV,
#             base_formats.HTML,
#         )

#         return [f for f in formats if f().can_export()]

#     def Mark_as_placed(self, modeladmin, news, queryset):
#         queryset.update(placed=True)

#     def Mark_as_not_placed(self, modeladmin, news, queryset):
#         queryset.update(placed=False)

#     actions = [
#         Mark_as_placed,
#         Mark_as_not_placed,
#     ]

class WaitlistAdmin(admin.ModelAdmin):
    form = MailingListForm
    list_display = ('building', 'view_applicants_link',)
    filter_horizontal = ("applicant", )
    
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "applicant":
            kwargs['queryset'] = Applicant.objects.filter(acad_details_verified=True, marriage_certificate_verified=True,
                                                        joint_photograph_with_spouse_verified=True,
                                                        coursework_grade_sheet_verified=True,
                                                        recommendation_of_guide_for_accomodation_verified=True)
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def view_applicants_link(self, obj):
        count = obj.applicant.count()
        url = (
            reverse("admin:portal_applicant_changelist")
            + "?"
            + urlencode({"waitlist__id": f"{obj.id}"})
        )

        return format_html('<a href="{}">{} Applicants</a>', url, count)

    view_applicants_link.short_description = "Applicants"

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        return response
    
class OccupiedListAdmin(admin.ModelAdmin):
    list_display = ('building', 'view_applicants_link',)
    filter_horizontal = ("applicant", )
    form = OccupiedListForm
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "applicant":
            kwargs['queryset'] = Applicant.objects.filter(acad_details_verified=True, marriage_certificate_verified=True,
                                                        joint_photograph_with_spouse_verified=True,
                                                        coursework_grade_sheet_verified=True,
                                                        recommendation_of_guide_for_accomodation_verified=True, waitlist__id__isnull=True)
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def view_applicants_link(self, obj):
        count = obj.applicant.count()
        url = (
            reverse("admin:portal_applicant_changelist")
            + "?"
            + urlencode({"occupiedlist__id": f"{obj.id}"})
        )

        return format_html('<a href="{}">{} Applicants</a>', url, count)

    view_applicants_link.short_description = "Applicants"

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        return response

class VacatedListAdmin(admin.ModelAdmin):
    list_display = ('building', 'view_applicants_link',)
    filter_horizontal = ("applicant",)
    form = VacatedListForm
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "applicant":
            kwargs['queryset'] = Applicant.objects.filter(Q(occupied_Type1=True) | Q(occupied_Tulsi=True) | Q(occupied_MRSB=True))
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def view_applicants_link(self, obj):
        count = obj.applicant.count()
        url = (
                reverse("admin:portal_applicant_changelist")
                + "?"
                + urlencode({"vacatedlist__id": f"{obj.id}"})
        )

        return format_html('<a href="{}">{} Applicants</a>', url, count)

    view_applicants_link.short_description = "Applicants"

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        return response


hcu_admin_site = HCUAdminSite(name='hcu_admin')
acad_admin_site = AcadAdminSite(name='acad_admin')
acad_admin_site.register(Applicant, AcadAdmin)
hcu_admin_site.register(Applicant, HCUAdmin)
hcu_admin_site.register(Waitlist, WaitlistAdmin)
hcu_admin_site.register(OccupiedList, OccupiedListAdmin)
hcu_admin_site.register(VacatedList, VacatedListAdmin)
admin.site.register(Applicant, ApplicantAdmin)
admin.site.register(Waitlist, WaitlistAdmin)
admin.site.register(OccupiedList, OccupiedListAdmin)
admin.site.register(VacatedList, VacatedListAdmin)