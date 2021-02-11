from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField, UsernameField, \
    PasswordResetForm
from django.forms import CheckboxSelectMultiple
from django_select2 import forms as s2forms

from .models import Recruit, UserPrimeTime, UserActivity, UserRole


class PasswordReset(PasswordResetForm):
    class Meta:
        model = get_user_model()
        fields = ('__all__',)


class CustomUserCreationForm(UserCreationForm):
    prime_time_fields = forms.MultipleChoiceField(
        label='Прайм-тайм',
        required=False,
        choices=[(c.pk, c.prime_time) for c in UserPrimeTime.objects.all()], widget=CheckboxSelectMultiple)

    activity_fields = forms.MultipleChoiceField(
        label='Активности',
        required=False,
        choices=[(c.pk, c.activity) for c in UserActivity.objects.all()], widget=CheckboxSelectMultiple)

    role_fields = forms.MultipleChoiceField(
        label='Роли',
        required=False,
        choices=[(c.pk, c.role_name) for c in UserRole.objects.all()], widget=CheckboxSelectMultiple)

    class Meta(UserCreationForm):
        model = get_user_model()
        fields = ('username', 'first_name', 'email', 'city', 'phone', 'timezone', 'password1', 'password2')


class UserEdit(UserChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['password']

    phone_hidden_fields = forms.BooleanField(label='Скрыть номер', required=False)
    email_hidden_fields = forms.BooleanField(label='Скрыть email', required=False)

    prime_time_fields = forms.MultipleChoiceField(
        label='Прайм-тайм',
        required=False,
        choices=[(c.pk, c.prime_time) for c in UserPrimeTime.objects.all()], widget=CheckboxSelectMultiple)

    activity_fields = forms.TypedMultipleChoiceField(
        label='Активности',
        required=False,
        choices=[(c.pk, c.activity) for c in UserActivity.objects.all()], widget=CheckboxSelectMultiple)

    role_fields = forms.MultipleChoiceField(
        label='Роли',
        required=False,
        choices=[(c.pk, c.role_name) for c in UserRole.objects.all()], widget=CheckboxSelectMultiple)

    class Meta:
        model = get_user_model()
        fields = (
            'first_name',
            'email',
            'timezone',
            'phone',
            'city'
        )


class MyActivationCodeForm(forms.Form):
    error_css_class = 'has-error'
    error_messages = {'password_incorrect':
                          ("Старый пароль не верный. Попробуйте еще раз.",),
                      'password_mismatch':
                          ("Пароли не совпадают.",),
                      'cod-no':
                          ("Код не совпадает.",), }

    def __init__(self, *args, **kwargs):
        super(MyActivationCodeForm, self).__init__(*args, **kwargs)

    code = forms.CharField(required=True, max_length=50, label='Код подтвержения',
                           widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                           error_messages={'required': 'Введите код!',
                                           'max_length': 'Максимальное количество символов 50'})

    def save(self, commit=True):
        profile = super(MyActivationCodeForm, self).save(commit=False)
        profile.code = self.cleaned_data['code']

        if commit:
            profile.save()
        return profile


class CustomUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label="Пароль",
        help_text=""" """)

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'email', 'password')
        field_classes = {'username': UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].help_text = self.fields['password'].help_text.format('../password/')
        f = self.fields.get('user_permissions')
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class RecruiterWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "username__icontains",
        "email__icontains",
    ]


class InviteeWidget(s2forms.ModelSelect2TagWidget):
    search_fields = [
        "username__icontains",
        "email__icontains",
    ]
    queryset = get_user_model().objects.all()

    def value_from_datadict(self, data, files, name):

        """Create objects for given non-pimary-key values. Return list of all primary keys."""

        values = set(super().value_from_datadict(data, files, name))
        # This may only work for MyModel, if MyModel has title field.
        # You need to implement this method yourself, to ensure proper object creation.
        registered_users = []
        users_ids = []
        users_names = []
        for value in values:
            try:
                users_ids.append(int(value))
            except ValueError:
                users_names.append(value)

        pks_ids = []
        uns_ids = []

        pks = self.queryset.filter(**{'id__in': list(users_ids)}).values_list('id', flat=True)
        uns = self.queryset.filter(**{'username__in': list(users_names)}).values_list('id', flat=True)

        for pk in pks:
            pks_ids.append(pk)

        for un in uns:
            uns_ids.append(un)

        for value in users_ids:
            if value in pks_ids:
                registered_users.append(value)
            else:
                users_names.append(value)

        for value in users_names:
            if value in uns_ids:
                registered_users.append(value)
            else:
                users_names.append(value)

        for value in users_names:
            new_user = self.queryset.create(username=value, password=f'TheDreams{value}')
            registered_users.append(new_user.id)

        return registered_users


class RecruitForm(forms.ModelForm):
    class Meta:
        model = Recruit
        fields = "__all__"
        widgets = {
            "recruiter": RecruiterWidget,
            "invitee": InviteeWidget,
        }
