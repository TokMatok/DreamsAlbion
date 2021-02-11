function montaURL(url, data) {
    let params = Object.keys(data).reduce(function (_qs, k, i) {
        if (data[k]) {
            return _qs + '&' + k + '=' + data[k];
        } else {
            return _qs + '&' + k + '=';
        }
    }, '').substring(1);
    url = url + "?" + params;
    return url
}


function update_payments_for_user(username) {
    let url = montaURL('/payments/get_payments_for_user', {"method": 'GET', "username": username});
    fetch(url)
        .then(function (response) {
            return response.json();
        }).then(function (data) {
        $("a#" + data.user_id).attr("data-original-title", data.payments)
        $("#sum" + data.user_id).text(data.summ)
        if (data.payments_for_me_confirmed) {
            $("#payments_for_me_confirmed").text(data.payments_for_me_confirmed)
        }
        if (data.payments_for_me_not_confirmed) {
            $("#payments_for_me_not_confirmed").text(data.payments_for_me_not_confirmed)

        }
    }).catch(function (ex) {
        console.log("parsing failed", ex);
    })
}


$(".change-state").click(function () {
    const element_id = $(this).attr('id');
    let payment_id = element_id.replace("status", '');
    let url = montaURL('/payments/set_payment_state', {'method': 'GET', 'payment_id': payment_id})
    fetch(url)
        .then(function (response) {
            return response.json();
        }).then(function (data) {
        if (data.successful) {
            $("#status" + payment_id).toggleClass("label-red label-green");
            if (data.current_status) {
                $("#status" + payment_id).text("Да");
            } else {
                $("#status" + payment_id).text("Нет");
            }
            update_payments_sum();
            let username = $.trim($("#status" + payment_id).parent().parent().children().first().text());
            console.log(username)
            update_payments_for_user(username);

        }
    }).catch(function (ex) {
        console.log("parsing failed", ex);
    })
})

function update_payments_sum() {
    let get_not_confirm = montaURL('/payments/get_sum_payments_not_confirm', {"method": 'GET'});
    let get_confirm = montaURL('/payments/get_sum_payments_confirm', {"method": 'GET'});

    fetch(get_not_confirm)
        .then(function (response) {
            return response.json();
        }).then(function (data) {
        $('#sum_payments_not_confirm').text(data.payment_amount__sum);
    }).catch(function (ex) {
        console.log("parsing failed", ex);
    });

    fetch(get_confirm)
        .then(function (response) {
            return response.json();
        }).then(function (data) {
        $('#sum_payments_confirm').text(data.payment_amount__sum);
    }).catch(function (ex) {
        console.log("parsing failed", ex);
    });

}

$('#search-btn').click(function () {
    let username = $("#username").val();
    let url = montaURL('/payments/get_debt', {"method": 'GET', "username": username});
    console.log(url);
    fetch(url)
        .then(function (response) {
            return response.json();
        }).then(function (data) {
        if (data.debt_error) {
            $('#searched-payments').text(data.debt_error);
        } else if (data.debt_to_player) {
            $('#searched-payments').text(" Не выплачено для " + data.username + ": " + data.debt_to_player);
        }
    }).catch(function (ex) {
        console.log("parsing failed", ex);
    });

});


$('.user').hover(
    $(this).tooltip({
        'html': true,
        delay: {show: 100, hide: 200},
        placement: function (tip, element) { //$this - экземпляр tooltip
            let position = $(element).position();
            /* если его left-координата меньше или равно 300px, то подсказку будем показывать снизу от элемента, иначе слева от элемента */
            if (position.left <= 300) {
                return "bottom";
            } else {
                return "right";
            }
        }

    }))
