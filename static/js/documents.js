$(document).ready(function(){
    // Click listener to toggle the Tags display
    $('#all-tags-btn').click(function(){
        $('#all-tags-container').toggle(300);
    });

    // Click listener to fire the document creation API call
    $('#doc-create-btn').click(function(){
        $(this).attr("disabled", true);
        $('#doc-create-spinner').removeClass('d-none');
        const HOME_URL = location.origin;

        tagList = [];
        tags = $('.tags');
        if (tags) {
            for (let tag = 0; tag < tags.length; tag++) {
                if (tags[tag].checked) {
                    tagList.push(tags[tag].value);
                }
            }
        }

        formData = {
            doc_type: $("input[name='doc_type']").val(),
            doc_title: $("input[name='doc_title']").val(),
            tag_list: tagList,
            extra_tags: $("input[name='extra_tags']").val(),
            categories: $("[name='categories']").val(),
        }

        // Fires the call to the backend to create the document
        fetch('/documents/create-document', {
            method: "POST",
            mode: 'same-origin',
            headers: {
                'X-CSRFToken': Cookies.get('csrftoken'),
                'X-Requested-With': 'XMLHttpRequest',
                "Content-type": "application/json; charset=UTF-8",
                "Accept": "application/json"
            },
            body: JSON.stringify(formData)
        })
        .then(response => {
            return response.json();
        })
        .then(data => {
            // Opens the newly created doc in a separate tab
            window.open(data['webViewLink'], '_blank');
            // Redirects the doc creation page to the Home page
            location.replace(HOME_URL);
        })
        .catch(error => {
            console.log(`Document creation failed: ${error}`);
            $('#creation-error').toggle();
        })
    });
});
