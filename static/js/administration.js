$(document).ready(function(){
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

    // Click listener to fire the switch toggler
    $('.slider-input').click(function(){
        switchToggle(this)
    });

    /* 
    * Click listener to handle the user dropdown. When a user is selected,
    * a call is made to the API on the backend to retrieve the corresponding
    * user's details. These are then used to prepopulate the form.
    */
    $('.user-option').click(function(){
        fetch(`/admin-area/user-data-api/${$(this).val()}`, {
            headers: {
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
            },
        })
        .then(response => {
            return response.json();
        })
        .then(data => {
            let users = JSON.parse(data);
            const fields = users[0]['fields'];
            $('#id_email').val(fields['email']);
            $('#id_first_name').val(fields['first_name']);
            $('#id_last_name').val(fields['last_name']);
            if (fields['is_staff'] == true) {
                $('#is-superuser').attr('checked', true);
            }
            else {
                $('#is-superuser').attr('checked', false);
            }
            if (fields['is_active'] == true) {
                $('#is-active').attr('checked', true);
            }
            else {
                $('#is-active').attr('checked', true);
            }
        })
        .catch(error => {
            console.log(`Ajax Error: ${error}`);
        })
    })
});