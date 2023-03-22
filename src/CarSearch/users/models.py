import os
from django.db import models
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core import validators
from django.conf import settings
from django.contrib.auth.models import BaseUserManager


class UserType(models.Model):
    type_id = models.IntegerField(primary_key=True)
    type_name = models.CharField(_('類別'), max_length=50)
    create_at = models.DateTimeField(default=timezone.now)
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                  related_name='user_type_create_at')

    def __str__(self):
        return self.type_name


class CustomUserManager(BaseUserManager):

    def _create_user(self, username, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not username:
            raise ValueError('The given username must be set')
        user = self.model(username=username,
                          is_staff=is_staff,
                          is_active=True,
                          is_superuser=is_superuser,
                          last_login=now,
                          date_joined=now,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        return self._create_user(username, password, False, False,
                                 **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        return self._create_user(username, password, True, True,
                                 **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('登入帳號'), max_length=30, unique=True,
                                validators=[
                                    validators.RegexValidator(r'^[\w.@+-]+$',
                                                              _('Enter a valid username. '
                                                                'This value may contain only letters, numbers '
                                                                'and @/./+/-/_ characters.'), 'invalid'),
                                ], error_messages={
                                    'unique': _("A user with that username already exists."),
    })
    nickname = models.CharField(_('名稱'), max_length=254)

    user_type = models.ForeignKey(UserType, related_name='user_type',null=True, on_delete=models.DO_NOTHING)
    mobile1 = models.CharField(_('手機1'), max_length=30, blank=False,
                                     validators=[validators.RegexValidator(r'^[0-9+()-]+$',
                                                                           _('Enter a valid mobile number.'),
                                                                           'invalid')])
    mobile2 = models.CharField(_('手機2'), max_length=30, blank=True,
                               validators=[validators.RegexValidator(r'^[0-9+()-]+$',
                                                                     _('Enter a valid mobile number.'),
                                                                     'invalid')])
    tel1 = models.CharField(_('連絡電話1'), max_length=30, blank=True,
                               validators=[validators.RegexValidator(r'^[0-9+()-]+$',
                                                                     _('Enter a valid mobile number.'),
                                                                     'invalid')])
    tel2 = models.CharField(_('連絡電話2'), max_length=30, blank=True,
                               validators=[validators.RegexValidator(r'^[0-9+()-]+$',
                                                                     _('Enter a valid mobile number.'),
                                                                     'invalid')])

    email1 = models.EmailField(_('Email1'), max_length=254, null=True, blank=True)
    email2 = models.EmailField(_('Email2'), max_length=254, null=True, blank=True)
    email3 = models.EmailField(_('Email3'), max_length=254, null=True, blank=True)
    email4 = models.EmailField(_('Email4'), max_length=254, null=True, blank=True)
    expired_date = models.DateTimeField(_('帳號到期日'), default=timezone.now)
    send_sms = models.BooleanField(_('簡訊通知'), default=False)
    send_email = models.BooleanField(_('Email通知'), default=False)
    note = models.TextField(_('備註'), max_length=254, null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True, editable=True)
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_dt',
                                  on_delete=models.DO_NOTHING)
    update_at = models.DateTimeField(auto_now=True, null=True)
    update_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_update_dt',
                                  on_delete=models.DO_NOTHING)

    # Admin 保留欄位
    is_active = models.BooleanField(_('啟用'), default=False)
    is_staff = models.BooleanField(_('is_staff'), default=False)
    date_joined = models.DateTimeField(_('建檔日期'), default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')


    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])


@receiver(models.signals.post_delete, sender=CustomUser)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.files:
        if os.path.isfile(instance.files.path):
            os.remove(instance.files.path)


class UserAuthority(models.Model):
    user = models.ForeignKey(CustomUser, related_name='user_authority', null=True, on_delete=models.CASCADE)
    CARTYPE = models.BooleanField(default=False)
    CARCOLOR = models.BooleanField(default=False)
    CARAGE = models.BooleanField(default=False)
    COMPANY = models.BooleanField(default=False)
    COMPANY2 = models.BooleanField(default=False)
    DEBIT = models.BooleanField(default=False)
    ENDDATE = models.BooleanField(default=False)
    ACCNO = models.BooleanField(default=False)
    GRADE = models.BooleanField(default=False)
    COMPMAN = models.BooleanField(default=False)
    CASENO = models.BooleanField(default=False)
    VDATE = models.BooleanField(default=False)
    FINDMODE = models.BooleanField(default=False)
    CHGDATE = models.BooleanField(default=False)
    CHGREC = models.BooleanField(default=False)
    NOTE2 = models.BooleanField(default=False)
    MAN = models.BooleanField(default=False)
    VID = models.BooleanField(default=False)
    ADDR1 = models.BooleanField(default=False)
    ADDR2 = models.BooleanField(default=False)
    ADDR3 = models.BooleanField(default=False)
    ADDR4 = models.BooleanField(default=False)
    TEL1 = models.BooleanField(default=False)
    TEL2 = models.BooleanField(default=False)
    TEL3 = models.BooleanField(default=False)
    TEL4 = models.BooleanField(default=False)
    OTH1 = models.BooleanField(default=False)
    OTH2 = models.BooleanField(default=False)
    OTH3 = models.BooleanField(default=False)
    OTH4 = models.BooleanField(default=False)
    DOWNLOAD_CAR_LIST = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True, editable=True)
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='auth_create_dt',
                                  on_delete=models.DO_NOTHING)
    update_at = models.DateTimeField(auto_now=True, null=True)
    update_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='auth_update_dt',
                                  on_delete=models.DO_NOTHING)