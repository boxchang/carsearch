from django import forms
from bootstrap_datepicker_plus.widgets import DatePickerInput
from crispy_forms.layout import Layout, Div
from crispy_forms.helper import FormHelper
# Regular form
from users.models import CustomUser


class FileDownloadForm(forms.Form):
    sales = forms.ModelChoiceField(required=False, label="SALES", queryset=CustomUser.objects.all(),
                                   widget=forms.Select(attrs={'class': "form-select"}))
    data_date_start = forms.CharField(required=False, label="時間(起)")
    data_date_end = forms.CharField(required=False, label="時間(迄)")

    def __init__(self, *args, submit_title='Submit', **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True

        self.helper.layout = Layout(
            Div(Div('sales', css_class='col-md-4'),
                Div('data_date_start', css_class='col-md-4'),
                Div('data_date_end', css_class='col-md-4'),
                css_class='row'),
        )

        self.fields['data_date_start'].widget = DatePickerInput(
            options={
                "format": "YYYY-MM-DD",
                "showClose": False,
                "showClear": False,
                "showTodayButton": False,
            }
        )

        self.fields['data_date_end'].widget = DatePickerInput(
            options={
                "format": "YYYY-MM-DD",
                "showClose": False,
                "showClear": False,
                "showTodayButton": False,
            }
        )