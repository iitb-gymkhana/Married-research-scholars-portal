from django import forms

from .models import Queuer


class QueuerForm(forms.ModelForm):
    """Form definition for Queuer."""

    def __init__(self, *args, **kwargs):
        super(QueuerForm, self).__init__(*args, **kwargs)
        # self.fields['roll_number'].disabled = True
        # self.fields['name'].disabled = True
        # self.fields['email'].disabled = True

    class Meta:
        model = Queuer
        fields = "__all__"
        exclude = (
            "placed",
            "waitlist_number",
        )


class QueuerAdminForm(forms.ModelForm):
    """Form definition for Queuer on admin page"""

    class Meta:
        model = Queuer
        fields = "__all__"
        exclude = ("waitlist_number",)
