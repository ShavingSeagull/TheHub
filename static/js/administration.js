/* jshint esversion: 6 */
$(document).ready(function(){
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
            $('#username').val(fields['username']);
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
                $('#is-active').attr('checked', false);
            }
        })
        .catch(error => {
            console.log(`Ajax Error: ${error}`);
        })
    })
});