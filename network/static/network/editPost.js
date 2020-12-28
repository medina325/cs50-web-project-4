function edit_post(edit_btn) {
    // Getting the "container" div of a post
    let card = document.getElementById(edit_btn.name);
        
    // Getting p tag childNode
    let p = card.querySelector('p');

    // Getting form tag childNode
    let edit_form = card.querySelector('form');

    // Creating textarea with post content to be edited and appending it to the form
    let edit_textarea = document.createElement('textarea');
    edit_textarea.className = 'edit_textarea';
    edit_textarea.autofocus = true;
    edit_textarea.innerHTML = p.innerHTML.replace(/<br>/g, '\n');
    edit_form.appendChild(edit_textarea);

    // Replacing post content with editable textarea
    p.replaceWith(edit_textarea);

    // Creating save (submit) button and appending it to the form
    let save_btn = document.createElement('button');
    save_btn.className = 'btn btn-success';
    save_btn.type = 'submit';
    save_btn.innerHTML = 'Save';
    edit_form.appendChild(save_btn);

    // Replacing edit button with save button
    edit_btn.replaceWith(save_btn);

    // Saving edited post in the database
    edit_form.onsubmit = () => {
                            
        fetch('/saveEditedPost', {
            method: 'PUT',
            body: JSON.stringify({
                edited_content: edit_textarea.value,
                post_id: edit_btn.name,
            })
        })
        .then(response => response.json())
        .then(result => {
            console.log(result);

            // Putting everything back
            save_btn.replaceWith(edit_btn);
            p.innerHTML = edit_textarea.value.replace(/\n/g, '<br>');
            edit_textarea.replaceWith(p);
        });
    
        return false;
    };
}
