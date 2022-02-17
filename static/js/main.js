/* jshint esversion: 6 */

/**
 * A small animation to render the main header first, then the subheader afterward.
 * The speeds are adjusted slightly for the major breakpoints, to avoid animations being too fast.
 */
function animateHeaders() {
    if($(window).width() > 900) {
        $('.page-header').animate({
            width: '50%'
        }, 1500, () => {
            $('.page-subheader').animate({
                width: '50%'
            }, 1700)
        });
    } else if($(window).width() > 576) {
        $('.page-header').animate({
            width: '100%'
        }, 1700, () => {
            $('.page-subheader').animate({
                width: '100%'
            }, 1600)
        });
    } else {
        $('.page-header').animate({
            width: '100%'
        }, 1600, () => {
            $('.page-subheader').animate({
                width: '100%'
            }, 1400)
        });
    }
}

/**
 * The toggle switch is a styled label via CSS. Therefore, the actual <input> checkbox
 * isn't able to be checked via mouse click. This click listener sets the state of the
 * <input> itself, so that the backend can retrieve it accurately.
 * @param {node} elem 
 */
 function switchToggle(elem) {
    if ($(elem).attr('checked')) {
        $(elem).attr('checked', false);
    } else {
        $(elem).attr('checked', true);
    }
}

// Calls the animation function only when the page is ready
$(document).ready(function(){
    animateHeaders();
});

/* Resets the widths and plays the animation again on active screen resizing.
*  This is primarily to avoid the headers causing overflow when switched from large to small screens.
*/
$(window).resize(function(){
    $('.page-header').css('width', '0');
    $('.page-subheader').css('width', '0');
    animateHeaders();
});

$('.selection-card').hover(function(){
    $(this).addClass('card-pulse');
    $(this).children('a').children('p').css('color', '#e84610');
}, function(){
    $(this).removeClass('card-pulse');
    $(this).children('a').children('p').css('color', '#4a4a4f');
});

// Click listener to fire the switch toggler
$('.slider-input').click(function(){
    switchToggle(this)
});
