$(document).ready(function(){
    // Click listener to toggle the Tags display
    $('#all-tags-btn').click(function(){
        $('#all-tags-container').toggle(300);
    });

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

        for (let i = 0; i < formData.length; i++) {
            console.log(`FORMDATA: ${i}`);
        }

        fetch('/documents/create-document-v2', {
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
            response.json();
            for (let y = 0; y < response.length; y++){
                console.log(`RESPONSE: ${response}`);
            }
        })
        .then(data => {
            let parsedData = JSON.parse(data);
            for (let x = 0; x < parsedData.length; x++){
                console.log(`DATA: ${x}`);
            }
        })
        .catch(error => {
            console.log(`Ajax Error: ${error}`);
        })
    });
});
