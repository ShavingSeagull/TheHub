$(document).ready(function(){
    // Click listener to toggle the Tags display
    $('#all-tags-btn').click(function(){
        $('#all-tags-container').toggle(300);
    });

    // Click listener to fire the document creation API call
    $('#doc-create-btn').click(function(){
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
            let parsedData = JSON.parse(data);
            window.open(parsedData['webViewLink'], '_blank');
        })
        .catch(error => {
            console.log(`Ajax Error: ${error}`);
        })
    });
});
