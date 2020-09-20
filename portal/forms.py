from django import forms

from .models import Queuer, Dependant


class QueuerForm(forms.ModelForm):
    """Form definition for Queuer."""

    def __init__(self, *args, **kwargs):
        super(QueuerForm, self).__init__(*args, **kwargs)
        # self.fields['roll_number'].disabled = True
        # self.fields['name'].disabled = True
        # self.fields['email'].disabled = True

    class Meta:
        model = Queuer
        fields = (
            # "building_applied",
            "name",
            "email",
            "roll_number",
            "contact_number",
            "spouse_name",
            # "dependant",
            "marriage_certificate",
            "your_aadhaar_card",
            "spouse_aadhaar_card",
        )

    dependant = forms.ModelChoiceField(Queuer.objects.filter(dependant__isnull=False), empty_label=None)


class QueuerAdminForm(forms.ModelForm):
    """Form definition for Queuer on admin page"""

    class Meta:
        model = Queuer
        fields = "__all__"
        exclude = ("waitlist_Type1","waitlist_Tulsi", "waitlist_MRSB")
