from django import forms
from django.contrib.auth import get_user_model
from django_select2 import forms as s2forms

from Payments.models import Treasurer, Payment


class TreasurerWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "username__icontains",
        "email__icontains",
    ]

    queryset = get_user_model().objects.filter(id__in=Treasurer.objects.all().values_list('treasurer_id'))

    def value_from_datadict(self, data, files, name):
        values = list(set(super().value_from_datadict(data, files, name)))
        return Treasurer.objects.filter(treasurer_id=values[0]).first()


class RecipientWidget(s2forms.ModelSelect2TagWidget):
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
            us = get_user_model().objects.filter(username=value).first()
            if us:
                if us.id in uns_ids:
                    registered_users.append(us.id)
                    users_names.remove(value)

        for value in users_names:
            new_user = self.queryset.create(username=value, password=f'TheDreams{value}')
            registered_users.append(new_user.id)

        return registered_users


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = "__all__"
        exclude = ["confirm"]
        widgets = {
            "treasurer": TreasurerWidget,
            "whom": RecipientWidget,
        }
