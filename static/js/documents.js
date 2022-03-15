/**
 * Wraps the API Fetch call into a function in order to implement
 * the ability to retry should the server suffer transient fails.
 * Code adapted from: https://stackoverflow.com/questions/55651169/javascript-fetch-returns-404-occasionally
 * Credit to T.J. Crowder for his solution.
 * @param {string} input 
 * @param {*} init 
 * @param {int} retries
 */
function uploadDoc(input, init, retries=10) {
    return fetch(input, init)
        .then(function(response) {
            if (response.ok) {
                return response.json();
            }
            throw new Error(`Response status: ${response.status}`);
        })
        .catch(error => {
            if (retries <= 0) {
                throw error;
            }
            return uploadDoc(input, init, retries - 1);
        });
}

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
        for (let tag = 0; tag < tags.length; tag++) {
            if (tags[tag].checked) {
                tagList.push(tags[tag].value);
            }
        }

        formData = {
            doc_type: $("input[name='doc_type']").val(),
            doc_title: $("input[name='doc_title']").val(),
            tag_list: tagList,
            extra_tags: $("input[name='extra_tags']").val(),
            categories: $("[name='categories']").val(),
        }

        uploadDoc('/documents/create-document', {
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
        .then(data => {
            if (data.Status === 'OK') {
                let parsedData = JSON.parse(data);
                // Opens the newly created doc in a separate tab
                window.open(parsedData['webViewLink'], '_blank');
                // Redirects the doc creation page to the Home page
                location.replace(HOME_URL);
            }
        })
        .catch(error => {
            console.log(`All API attempts failed: ${error}`);
        })
    });
});
