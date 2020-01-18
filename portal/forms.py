from django import forms

from .models import Queuer


class QueuerForm(forms.ModelForm):
    """Form definition for Queuer."""

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
