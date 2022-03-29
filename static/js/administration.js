/* jshint esversion: 6 */
$(document).ready(function(){
    /* 
       ------------------
        ADMIN USER PAGES
       ------------------
    */

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
    });

    /*
    Click listener removes the disabled attribute on the submit button if
    the input has a value within it - want to prevent submission of the form
    if an option isn't selected from the Users dropdown menu.
    */
    $('#users').click(function(){
        if ($(this).val()) {
            $('input[type=submit]').attr("disabled", false);
        } else {
            $('input[type=submit]').attr("disabled", true);
        }
    });

    /* 
       ----------------------
        ADMIN CATEGORY PAGES
       ----------------------
    */
    let currentPage = location.pathname;
    let btnValue;
    let btnCheckedValue;

    if (currentPage.includes("create-category")) {
        btnValue = "Create";
        btnCheckedValue = "add";
    } else if (currentPage.includes("edit-category")) {
        btnValue = "Edit";
        btnCheckedValue = "edit";
    }
    
    /*
    Alters the label on the create_category template to say
    'Name' rather than the actual field name of 'Friendly Name'.
    Form is generated by Crispy.
    */
    $('#div_id_friendly_name > label').text("Name*");

    /*
    Changes the value of the submit button based on whether the 
    checbox to add another category is checked
    */
    $('#another-category').click(function(){
        if (this.checked) {
            $('input[type=submit]').val(`Save and ${btnCheckedValue} another`);
        } else {
            $('input[type=submit]').val(`${btnValue} category`);
        }
    });

    // Prepopulates the input field with the category name from the dropdown menu
    $('.category-option').click(function(){
        $('#id_friendly_name').val($(this).text());
    });

    /*
    Click listener removes the disabled attribute on the submit button if
    the input has a value within it - want to prevent submission of the form
    if an option isn't selected from the Categories dropdown menu.
    */
    $('#categories').click(function(){
        if ($(this).val()) {
            $('input[type=submit]').attr("disabled", false);
        } else {
            $('input[type=submit]').attr("disabled", true);
        }
    });
});