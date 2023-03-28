from django import forms
from bootstrap_datepicker_plus.widgets import DatePickerInput
from crispy_forms.layout import Layout, Div
from crispy_forms.helper import FormHelper
# Regular form
from users.models import CustomUser


class FileUploadForm(forms.Form):
    file = forms.FileField(label="", widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))

    def clean_file(self):
        file = self.cleaned_data['file']
        ext = file.name.split('.')[-1].lower()
        if ext not in ["dbf"]:
            raise forms.ValidationError("Only dbf files are allowed.")
        # return cleaned data is very important.
        return file



