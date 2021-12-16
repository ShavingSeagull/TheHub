/* jshint esversion: 6 */
const SIDENAV = $('#sidenav');
const NAVPROFILE = $('.sidenav-profile');
const NAVLISTHIDDENELEMS = $('#sidenav-list').children('li').children('a').children('p');
const BURGERMENU = $('#burger-menu');
const OVERLAY = $('#sidenav-overlay');

/**
 * Hides the navbar elements, apart from the FontAwesome logo for each nav link.
 */
function hideElements() {
    OVERLAY.addClass('d-none');
    NAVLISTHIDDENELEMS.addClass('d-none');
    NAVPROFILE.addClass('d-none');
}

/**
 * Shows the entirety of the navbar elements.
 */
function showElements() {
    NAVLISTHIDDENELEMS.removeClass('d-none');
    NAVPROFILE.removeClass('d-none');
}

/**
 * Handles the expanding width of the navbar for small screens.
 */
function expandSmallerScreens() {
    SIDENAV.css('width', '250px');
    OVERLAY.removeClass('d-none');
}

/**
 * Handles the positioning of the navbar on mobile sized devices.
 * Note: mobile devices utilize a different style of navbar that moves rather than expands
 */
function expandMobile() {
    SIDENAV.css('left', '0');
    OVERLAY.removeClass('d-none');
}

/**
 * Handles the expanding width of the navbar on larger screens.
 */
function expandDesktop() {
    SIDENAV.css('width', '270px');
    OVERLAY.removeClass('d-none');
}

/**
 * Alters the burger menu colouring and shading according to screen size.
 * The colouring will only need to change on small screens (under 576px), 
 * as it utilizes a different style of navbar and top bar.
 * 
 * The 'resize' param denotes if the function is being run due to the window
 * being actively resized or not - if it is, the default coolouring and shading
 * values just need to be reset and nothing else checked; the checks only need
 * to occur for normal usage of the navbar on smaller devices.
 * 
 * Note: without the 'resize' param, the burger menu will alternate/flash between
 * the dark and light colours at every pixel if the window is actively resized
 * via mouse dragging and may end up the incorrect colour when the window has 
 * finished resizing.
 * @param {bool} resize 
 */
function changeBurgerMenuColour(resize=false) {
    if ($(window).width() < 576) {
        if (resize) {
            BURGERMENU.children('a').css('color', '#fff');
            BURGERMENU.children('a').css('text-shadow', '#4a4a4f 2px 2px 2px');
        } else {
            if (BURGERMENU.children('a').css('color') == '#fff' || BURGERMENU.children('a').css('color') == 'rgb(255, 255, 255)') {
                BURGERMENU.children('a').css('color', '#4a4a4f');
                BURGERMENU.children('a').css('text-shadow', 'none');
            } else if (BURGERMENU.children('a').css('color') == '#4a4a4f' || BURGERMENU.children('a').css('color') == 'rgb(74, 74, 79)') {
                BURGERMENU.children('a').css('color', '#fff');
                BURGERMENU.children('a').css('text-shadow', '#4a4a4f 2px 2px 2px');
            }
        }
    } else {
        if (resize) {
            // Resets the colouring for larger screens. Useful mostly for windows that are actively resized
            BURGERMENU.children('a').css('color', '#4a4a4f');
            BURGERMENU.children('a').css('text-shadow', 'none');
        }
    }
}

// Click listener for the burger menu. Accounts for the three major breakpoints.
BURGERMENU.click(function(){
    if ($(window).width() < 576) {
        if (SIDENAV.position().left == -260) {
            expandMobile();
            showElements();
            changeBurgerMenuColour();
        } else {
            SIDENAV.css('left', '-260px');
            hideElements();
            changeBurgerMenuColour();
        }
    } else if ($(window).width() < 992) {
        if (SIDENAV.width() == 50) {
            expandSmallerScreens();
            setTimeout(showElements, 380);
        } else {
            SIDENAV.css('width', '50px');
            hideElements();
        }
    } else {
        if (SIDENAV.width() == 70) {
            expandDesktop();
            setTimeout(showElements, 440);
        } else {
            SIDENAV.css('width', '70px');
            hideElements();
        }
    }
});

// Click listener to close the navbar if the overlay is clicked
OVERLAY.click(function() {
    if ($(window).width() < 576) {
        SIDENAV.css('left', '-260px');
        hideElements();
        changeBurgerMenuColour();
    } else if ($(window).width() < 992) {
        SIDENAV.css('width', '50px');
        hideElements();
    } else {
        SIDENAV.css('width', '70px');
        hideElements();
    }
});

/*
Resize method is needed to prevent the media queries failing to fire if the CSS has been set via the click
events above. Only applies to windows being actively changed in size - fine either way on initial page load.
Unlikely to be required much, but a failsafe just in case.
 */
$(window).resize(function(){
    if ($(window).width() < 576) {
        SIDENAV.css('left', '-260px')
        SIDENAV.css('width', '250px');
        hideElements();
    } else if ($(window).width() < 992) {
        SIDENAV.css('left', '0');
        SIDENAV.css('width', '50px');
        hideElements();
    } else {
        SIDENAV.css('left', '0');
        SIDENAV.css('width', '70px');
        hideElements();
    }
    changeBurgerMenuColour(true);
});