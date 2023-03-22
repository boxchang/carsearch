from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import *
 # extend Django's built-in UserCreationForm and UserChangeForm to
 # remove the username field (and optionally add any others that are
 # required)

class CustomUserCreationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """

    def __init__(self, *args, **kargs):
        super(CustomUserCreationForm, self).__init__(*args, **kargs)


    class Meta:
        model = CustomUser
        fields = '__all__'

class CustomUserChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    def __init__(self, *args, **kargs):
        super(CustomUserChangeForm, self).__init__(*args, **kargs)

    class Meta:
        model = CustomUser
        fields = '__all__'

# ======================================================
 # Forms for users themselves edit their profiles
 # ======================================================
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, HTML, Field
from .models import CustomUser


class CurrentCustomUserForm(forms.ModelForm):
    user_type = forms.ModelChoiceField(label="類別", queryset=UserType.objects.all(), widget=forms.Select(
        attrs={'class': "form-select"}))
    send_sms = forms.BooleanField(label="簡訊通知", required=False, widget=forms.CheckboxInput(attrs={'class': "form-check-input"}))
    send_email = forms.BooleanField(label="Email通知", required=False, widget=forms.CheckboxInput(attrs={'class': "form-check-input"}))
    is_active = forms.BooleanField(label="是否啟用", required=False, widget=forms.CheckboxInput(attrs={'class': "form-check-input"}))
    password1 = forms.CharField(label="密碼", required=False, widget=forms.PasswordInput(attrs={'placeholder': '請輸入登入密碼'}))
    password2 = forms.CharField(label="確認密碼", required=False, widget=forms.PasswordInput(attrs={'placeholder': '請再次輸入登入密碼'}))
    tel1 = forms.CharField(label="連絡電話1", required=False, widget=forms.TextInput(attrs={'placeholder': '請輸入市話(含區碼)，例071234567'}))
    tel2 = forms.CharField(label="連絡電話2", required=False, widget=forms.TextInput(attrs={'placeholder': '請輸入市話(含區碼)，例071234567'}))
    username = forms.CharField(label="登入帳號", widget=forms.TextInput(attrs={'placeholder': '請輸入市話(含區碼)或手機'}))

    class Meta:
        model = CustomUser
        fields = ('username', 'user_type', 'nickname', 'password', 'mobile1', 'mobile2',
                  'tel1', 'tel2', 'email1', 'email2', 'email3', 'email4', 'expired_date',
                  'send_sms', 'send_email', 'note', 'is_active', 'password1', 'password2')
        widgets = {
            'note': forms.Textarea(attrs={'rows': 4, 'cols': 15}),
        }

    def __init__(self, *args, submit_title="儲存編輯", **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True
        self.fields['password'].required = False
        self.fields['expired_date'].required = False
        #self.helper.add_input(Submit('submit', submit_title))

        self.helper.layout = Layout(
            Div(
                Div('user_type', css_class="col-sm-4"),
                Div('nickname', css_class="col-sm-4"),
                Div(
                    HTML('<div class="form-switch">'),
                    Field('is_active'),
                    HTML('</div>'), css_class='col-md-2 text-center'),
                css_class='row'
            ),
            Div(
                Div('mobile1', css_class="col-sm-4"),
                Div('mobile2', css_class="col-sm-4"),
                Div(
                    HTML('<div class="form-switch">'),
                    Field('send_sms'),
                    HTML('</div>'), css_class='col-md-2 text-center'),
                Div(HTML('<div class="form-switch">'),
                    Field('send_email'),
                    HTML('</div>'), css_class="col-sm-2"),
                css_class='row'
            ),
            Div(
                Div('tel1', css_class="col-sm-4"),
                Div('tel2', css_class="col-sm-4"),
                css_class='row'
            ),
            Div(
                Div('email1', css_class="col-sm-12"),
                css_class='row'
            ),
            Div(
                Div('email2', css_class="col-sm-12"),
                css_class='row'
            ),
            Div(
                Div('email3', css_class="col-sm-12"),
                css_class='row'
            ),
            Div(
                Div('email4', css_class="col-sm-12"),
                css_class='row'
            ),
            Div(
                Div('username', css_class="col-sm-3"),
                Div('password1', css_class="col-sm-4"),
                Div('password2', css_class="col-sm-4"),
                css_class='row'
            ),
            Div(
                Div('note', css_class="col-sm-12"),
                css_class='row'
            ),
        )

    def clean(self):
        cleaned_data = super(CurrentCustomUserForm, self).clean()
        password = cleaned_data.get("password1")
        confirm_password = cleaned_data.get("password2")

        if password != confirm_password:
            raise forms.ValidationError(
                "密碼與確認密碼不一致"
            )
