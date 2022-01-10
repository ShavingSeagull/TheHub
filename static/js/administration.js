$(document).ready(function(){
    const ADMINSWITCH = $('#is-superuser');

    /* 
    * The toggle switch is a styled label via CSS. Therefore, the actual <input> checkbox
    * isn't able to be checked via mouse click. This click listener sets the state of the
    * <input> itself, so that the backend can retrieve it accurately.
    */
    ADMINSWITCH.click(function(){
        if (ADMINSWITCH.attr('checked')) {
            ADMINSWITCH.attr('checked', false);
        } else {
            ADMINSWITCH.attr('checked', true);
        }
    });
});