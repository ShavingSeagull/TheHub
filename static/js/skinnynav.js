/* jshint esversion: 6 */
const SIDENAV = $('#sidenav');
const NAVPROFILE = $('.sidenav-profile');
const NAVLISTHIDDENELEMS = $('#sidenav-list').children('li').children('a').children('p');
const BURGERMENU = $('#burger-menu');
const OVERLAY = $('#sidenav-overlay');

function hideElements() {
    OVERLAY.addClass('d-none');
    NAVLISTHIDDENELEMS.addClass('d-none');
    NAVPROFILE.addClass('d-none');
}

function showElements() {
    NAVLISTHIDDENELEMS.removeClass('d-none');
    NAVPROFILE.removeClass('d-none');
}

function expandMobileSkinny() {
    SIDENAV.css('width', '250px');
    OVERLAY.removeClass('d-none');
}

function expandDesktopSkinny() {
    SIDENAV.css('width', '270px');
    OVERLAY.removeClass('d-none');
}

BURGERMENU.click(function(){
    if ($(window).width() < 992) {
        if (SIDENAV.width() == 50) {
            expandMobileSkinny();
            setTimeout(showElements, 380);
        } else {
            SIDENAV.css('width', '50px');
            hideElements();
        }
    } else {
        if (SIDENAV.width() == 70) {
            expandDesktopSkinny();
            setTimeout(showElements, 440);
        } else {
            SIDENAV.css('width', '70px');
            hideElements();
        }
    }
});

// Click listener to close the navbar if the overlay is clicked
OVERLAY.click(function() {
    if ($(window).width() < 992) {
        SIDENAV.css('width', '50px');
        hideElements();
    } else {
        SIDENAV.css('width', '70px');
        hideElements();
    }
});

// Resize method is needed to prevent the media queries failing to fire if the CSS has been set via the click
// events above. Only applies to windows being actively changed in size - fine either way on initial page load. 
// Unlikely to be required much, but a failsafe just in case.
$(window).resize(function(){
    if ($(window).width() < 992) {
        SIDENAV.css('width', '50px');
        hideElements();
    } else {
        SIDENAV.css('width', '70px');
        hideElements();
    }
});