/* jshint esversion: 6 */

/* A small animation to render the main header first, then the subheader afterward.
*  The speeds are adjusted slightly for the major breakpoints, to avoid animations being too fast.
*/
$(document).ready(function(){
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
});