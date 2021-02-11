function divideNumberByPieces(x, delimiter) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, delimiter || " ");
}


$(function () {
    $('.user').tooltip({
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

    });
})

