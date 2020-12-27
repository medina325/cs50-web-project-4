document.addEventListener('DOMContentLoaded', function() {

    // New post form handler
    document.querySelector('#new_post_form').onsubmit = () => new_post();

    var edit_buttons = document.querySelectorAll('.btn.btn-primary.edit_btn');
    if (edit_buttons)
    {
        edit_buttons.forEach((edit_btn) => {
            edit_btn.addEventListener('click', () => edit_post(edit_btn));
        });
    }
    
    // Like and unlike button handlers
    document.querySelectorAll('.like').forEach(like_button => {
        like_button.onclick = () => like(like_button);
    });

    document.querySelectorAll('.unlike').forEach(unlike_button => {
        unlike_button.onclick = () => unlike(unlike_button);
    });
    
});

function new_post() {
    let newpost_textarea = document.querySelector("#textarea_new_post");

    fetch('/newPost', {
        method: 'POST',
        body: JSON.stringify({
            content: newpost_textarea.value,
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result['message']);

        let page_number = document.querySelector('#page_number');
        // The new post is only appended to the current page if that's the first page
        if (page_number.value === '1') {
            const newpost = result["newpost"];

            let div_card = document.createElement('div');
            div_card.className = 'card bg-dark border-light mb-3';
            div_card.innerHTML = `
            <div class="card-body">
                <li class="media">
                    <img src=${newpost.url} class="mr-4" alt="profile-pic" height="50px" width="50px" style="border-radius: 100px;">
                    <div id=${newpost.id} class="media-body">
                        <h6>${newpost.poster} said:</h6>
                        <p class="post_content">${newpost.content.replace(/\n/g, '<br>')}</p>
                        <hr>
                       
                        <form id="new_edit_form" class="edit_save_form">
                            
                        </form>
                        
                        <small class="text-muted">Posted on ${newpost.creation_date}</small>
                        <div>${newpost.number_likes} likes</div>
                    </div>
                </li>
            </div>
            `;     
    
            // Append the new post and clean the textarea
            document.querySelector('.new_post_div').prepend(div_card);
            newpost_textarea.value = '';
        
            // At least the edit button is created separetely to add the event listener to it
            // and then it's appended to the form inside the post
            let new_edit_btn = document.createElement('button');
            new_edit_btn.name = newpost.id;
            new_edit_btn.className = 'btn btn-primary edit_btn';
            new_edit_btn.innerHTML = 'Edit';
            new_edit_btn.addEventListener('click', () => edit_post(new_edit_btn));
    
            let form = document.getElementById('new_edit_form');
            form.appendChild(new_edit_btn);
        }  
    });

    return false;
}
