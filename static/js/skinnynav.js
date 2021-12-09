/* jshint esversion: 6 */
const SKINNYNAV = $('#skinny-nav');


// Resize method is needed to prevent the media queries failing to fire if the CSS has been set via the click
// events above. Only applies to windows being actively changed in size - fine either way on initial page load. 
// Unlikely to be required much, but a failsafe just in case.
$(window).resize(function(){
    if ($(window).width() < 992) {
        SKINNYNAV.css('width', '50px');
        hideElements();
    } else {
        SKINNYNAV.css('width', '70px');
        hideElements();
    }
});