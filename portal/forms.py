from django import forms
from .models import Applicant
class ApplicantForm(forms.ModelForm):
    """Form Definition for Applicant"""
    def __init__(self, *args, **kwargs):
        super(ApplicantForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            self.fields[key].required = True

    class Meta:
        model = Applicant
        fields = '__all__'
        exclude = (
            'marriage_certificate_verified',
            'joint_photograph_with_spouse_verified',
            'coursework_grade_sheet_verified',
            'recommendation_of_guide_for_accomodation_verified',
            'feedback',
            'waitlist_Type1',
            'waitlist_Tulsi',
            'waitlist_MRSB',
            'date_applied',
            'verified_time',
            'occupied_Type1',
            'occupied_Tulsi',
            'occupied_MRSB',
            'defer_Type1',
            'defer_Tulsi',
            'defer_MRSB'
        )
        widgets = {
            'date_of_marriage' : forms.SelectDateWidget,
            'date_of_registration' : forms.SelectDateWidget,
            'date_of_scholarship' : forms.SelectDateWidget,
            'course_work_completed_on' : forms.SelectDateWidget
        }

class OccupyingForm(forms.ModelForm):
    """Form Definition for Occupying"""
    def __init__(self, *args, **kwargs):
        super(OccupyingForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Applicant
        exclude = '__all__'
        fields = (
            'occupied_Type1',
            'occupied_Tulsi',
            'occupied_MRSB',
            'defer_Type1',
            'defer_Tulsi',
            'defer_MRSB'
        )
        labels = {
            "occupied_Type1": "Occupy Type-1",
            "occupied_Tulsi": "Occupy Tulsi",
            "occupied_MRSB": "Occupy MRSB",
            "defer_Tulsi": "Don't want Type-1",
            "defer_Type1": "Don't want Tulsi",
            "defer_MRSB": "Don't want MRSB"
        }


class VacatingForm(forms.Form):
    """Form definition for Vacating"""
    vacate = forms.BooleanField(label="Vacate your apartment",required=True)
