from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render, redirect

from TheDreams.apps.statistic.services.text_modifications import triad_format
from changelog.templatetags.custom_template_tag import is_group, completed_payments, load_payments, millennium_format
from .forms import PaymentForm
from .models import Payment, Treasurer


# TODO Добавить кнопку подтверждения всех выплат


def get_sum_payments_confirm(request=None):
    data = {"payment_amount__sum": 0}
    sum_ = triad_format(str(Payment.objects.filter(confirm=True).aggregate(
        Sum('payment_amount'))['payment_amount__sum']))
    data['payment_amount__sum'] = sum_
    if request:
        return JsonResponse(data)
    else:
        return sum_


def get_sum_payments_not_confirm(request=None):
    data = {"payment_amount__sum": 0}
    sum_ = triad_format(str(Payment.objects.filter(confirm=False).aggregate(
        Sum('payment_amount'))['payment_amount__sum']))
    data['payment_amount__sum'] = sum_
    if request:
        return JsonResponse(data)
    else:
        return sum_


def get_payments_for_me_confirmed(user):
    return Payment.objects.filter(whom=user, confirm=True).aggregate(
        Sum('payment_amount'))['payment_amount__sum']


def get_payments_for_me_not_confirmed(user):
    return Payment.objects.filter(whom=user, confirm=False).aggregate(
        Sum('payment_amount'))['payment_amount__sum']


def index(request):
    payments = Payment.objects.order_by('-date')
    users = get_user_model().objects.order_by('username')

    sum_payments_confirm = get_sum_payments_confirm()
    sum_payments_not_confirm = get_sum_payments_not_confirm()

    if request.user.is_authenticated:
        payments_for_me_confirmed = get_payments_for_me_confirmed(request.user)
        payments_for_me_not_confirmed = get_payments_for_me_not_confirmed(request.user)
    else:
        payments_for_me_confirmed = None
        payments_for_me_not_confirmed = None

    return render(request,
                  'Payments/index.html',
                  context={"page_title": 'Выплаты',
                           'payments': payments,
                           'users': users,
                           "sum_payments_confirm": sum_payments_confirm,
                           "sum_payments_not_confirm": sum_payments_not_confirm,
                           'payments_for_me_confirmed': payments_for_me_confirmed,
                           'payments_for_me_not_confirmed': payments_for_me_not_confirmed,
                           }
                  )


def set_payment_state(request):
    data = {'successful': False, 'current_status': False}

    if is_group(request.user, 'Казначей') or is_group(request.user, 'admin') or is_group(request.user,
                                                                                         'Глава казначеев'):

        payment_id = request.GET.get('payment_id')
        if payment_id:
            payment = Payment.objects.filter(id=payment_id).first()
            if payment:
                data['current_status'] = not payment.confirm
                payment.confirm = not payment.confirm
                data['successful'] = True
                payment.save()
            else:
                data['successful'] = False

    return JsonResponse(data)


def get_payments_for_user(request):
    data = {"payments": "", "summ": "0", "user_id": 0, 'payments_for_me_confirmed': None,
            'payments_for_me_not_confirmed': None}
    username = request.GET.get('username')
    user = get_user_model().objects.filter(username=username).first()

    if user == request.user:
        data['payments_for_me_confirmed'] = triad_format(str(get_payments_for_me_confirmed(user)))
        data['payments_for_me_not_confirmed'] = triad_format(str(get_payments_for_me_not_confirmed(user)))

    data['user_id'] = user.id
    if completed_payments(user):
        for payment in load_payments(user):
            data['payments'] += millennium_format(payment.payment_amount) + "<br>"
    else:
        data['payments'] = "Нет выплат"
    data["summ"] = triad_format(completed_payments(user))
    return JsonResponse(data)


def get_debt(request):
    data = {'debt_to_player': '', 'debt_error': ''}
    username = request.GET.get('username')

    if username:
        user = get_user_model().objects.filter(username=username).first()
        if user:
            exists = Payment.objects.filter(whom=user.id, confirm=False)
            if exists.exists():
                payments_for_user = exists.aggregate(Sum('payment_amount'))['payment_amount__sum']
                data['debt_to_player'] = triad_format(payments_for_user)

            else:
                data['debt_to_player'] = ' 0'
        else:
            data['debt_error'] = username + ' не найден.'
    else:
        data['debt_error'] = ' Ничего не указано.'
    data['username'] = username
    return JsonResponse(data)


def add_payment(request):
    if not is_group(request.user, 'Рекрутёр') and not is_group(request.user, 'admin') and not is_group(request.user,
                                                                                                       'Глава казначеев'):
        return redirect('/')
    else:
        treasurers = Treasurer.objects.all()
        if request.method == "POST":
            form = PaymentForm(request.POST)
            if "whom" in form.errors:
                form.errors.pop("whom")
            if form.is_valid():
                for user_id in form.data.getlist('whom'):
                    Payment.objects.create(whom_id=user_id, treasurer_id=form.cleaned_data['treasurer'].id,
                                           payment_amount=form.cleaned_data['payment_amount'],
                                           comment=form.cleaned_data['comment'], date=form.cleaned_data['date'])
                    # for user in form.
                return render(request,
                              "Payments/add_payment.html",
                              context={'page_title': "Добавить выплату", 'form': form, 'treasurers': treasurers})

            else:
                return render(request,
                              "Payments/add_payment.html",
                              context={'page_title': "Добавить выплату", 'form': form, 'treasurers': treasurers})
        else:
            form = PaymentForm()
            return render(request,
                          "Payments/add_payment.html",
                          context={'page_title': "Добавить выплату", 'form': form, 'treasurers': treasurers})
