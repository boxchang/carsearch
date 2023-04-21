from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div
from bases.models import EmailSetting


class SettingForm(forms.Form):
    server = forms.CharField()
    port = forms.IntegerField()
    account = forms.CharField()
    password = forms.CharField(required=False, widget=forms.PasswordInput())
    mail_from = forms.CharField(required=False)
    subject = forms.CharField(required=False)
    mail_body = forms.CharField(widget=forms.Textarea, required=False, max_length=20)

    class Meta:
        model = EmailSetting
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True

        self.helper.layout = Layout(
            Div('server', css_class='row'),
            Div('port', css_class='row'),
            Div('account', css_class='row'),
            Div('password', css_class='row'),
            Div('mail_from', css_class='row'),
            Div('subject', css_class='row'),
            Div('mail_body', css_class='row'),
        )
