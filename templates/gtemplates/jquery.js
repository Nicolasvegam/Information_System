$(function () {
    $(window).scroll(function () {
        if ($(this).scrollTop() > 20) {
            $('.nav').addClass('nav-pin').fadeIn();
        } else {
            $('.nav').removeClass('nav-pin');
        }
    });
});