/* jshint esversion: 6 */
const SKINNYNAV = $('#skinny-nav');
const SKINNYPROFILE = $('.skinny-nav-profile');
const SKINNYLISTHIDDENELEMS = $('#skinny-nav-list').children('li').children('a').children('p');
const BURGERMENU = $('#burger-menu');

function hideElements() {
    // OVERLAY.addClass('d-none');
    SKINNYLISTHIDDENELEMS.addClass('d-none');
    SKINNYPROFILE.addClass('d-none');
}

function showElements() {
    SKINNYLISTHIDDENELEMS.removeClass('d-none');
    SKINNYPROFILE.removeClass('d-none');
}

function expandMobileSkinny() {
    SKINNYNAV.css('width', '250px');
    // OVERLAY.removeClass('d-none');
}

function expandDesktopSkinny() {
    SKINNYNAV.css('width', '270px');
    // OVERLAY.removeClass('d-none');
}

BURGERMENU.click(function(){
    if ($(window).width() < 992) {
        if (SKINNYNAV.width() == 50) {
            expandMobileSkinny();
            setTimeout(showElements, 380);
        } else {
            SKINNYNAV.css('width', '50px');
            hideElements();
        }
    } else {
        if (SKINNYNAV.width() == 70) {
            expandDesktopSkinny();
            setTimeout(showElements, 440);
        } else {
            SKINNYNAV.css('width', '70px');
            hideElements();
        }
    }
})

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