/* jshint esversion: 6 */

/**
 * A small animation to render the main header first, then the subheader afterward.
 * The speeds are adjusted slightly for the major breakpoints, to avoid animations being too fast.
 */
function animateHeaders() {
    if($(window).width() > 900) {
        $('#home-header').animate({
            width: '50%'
        }, 1500, () => {
            $('#home-subheader').animate({
                width: '50%'
            }, 1700)
        });
    } else if($(window).width() > 576) {
        $('#home-header').animate({
            width: '100%'
        }, 1700, () => {
            $('#home-subheader').animate({
                width: '100%'
            }, 1600)
        });
    } else {
        $('#home-header').animate({
            width: '100%'
        }, 1600, () => {
            $('#home-subheader').animate({
                width: '100%'
            }, 1400)
        });
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
    $('#home-header').css('width', '0');
    $('#home-subheader').css('width', '0');
    animateHeaders();
});

$('.home-card').hover(function(){
    $(this).addClass('card-pulse');
    $(this).children('p').css('color', '#e84610');
}, function(){
    $(this).removeClass('card-pulse');
    $(this).children('p').css('color', '#4a4a4f');
});