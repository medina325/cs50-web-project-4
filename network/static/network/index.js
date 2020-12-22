document.addEventListener('DOMContentLoaded', function() {

    let newpost_form = document.querySelector('#new_post_form')
    if(newpost_form)
        newpost_form.onsubmit = () => new_post();

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
            content: newpost_textarea.value.replace(/\n/g, '<br>'),
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result['message']);
        const newpost = result["newpost"];

        let div_card = document.createElement('div');
        div_card.className = 'card bg-dark border-light mb-3';
        div_card.innerHTML = `
        <div class="card-body">
            <li class="media">
                <img src=${newpost.url} class="mr-4" alt="profile-pic" height="50px" width="50px" style="border-radius: 100px;">
                <div id={{ post.id }} class="media-body">
                    <h6>${newpost.poster} said:</h6>
                    <p class="post_content">${newpost.content}</p>
                    <hr>
                   
                    <form class="edit_save_form">
                        <button name=${newpost.id} class="btn btn-primary edit_btn">Edit</button>
                    </form>
                    
                    <small class="text-muted">Posted on ${newpost.creation_date}</small>
                    <div>${newpost.number_likes} likes</div>
                </div>
            </li>
        </div>
        `;     

        document.querySelector('.new_post_div').prepend(div_card);
        newpost_textarea.value = '';
    });

    return false;
}

function like(like_btn) {
    let parent = like_btn.parentNode;

    fetch('/likeunlike', {
        method: 'PUT',
        body: JSON.stringify({
            flag: 1, // meaning to like 
            target_post: parent.className,
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);

        // Replacing like button for unlike button
        let new_unlike_button = document.createElement('a');
        new_unlike_button.className = 'unlike';
        new_unlike_button.href = '#';
        new_unlike_button.innerHTML = `
        <img src="/static/network/un_like.png" alt="ain" height="40rem" width="40rem" style="opacity: 30%;">
        `;
        
        parent.appendChild(new_unlike_button);
        like_btn.remove();
    
        // Increase number of likes by 1
        let like_strong_tag = parent.getElementsByClassName(parent.className);
        let n_likes = parseInt(like_strong_tag[0].innerHTML);
        like_strong_tag[0].innerHTML = n_likes + 1;

        new_unlike_button.addEventListener('click', function() {
            unlike(new_unlike_button);
        });
    });
}

function unlike(unlike_btn) {
    let parent = unlike_btn.parentNode;
    
    fetch('/likeunlike', {
        method: 'PUT',
        body: JSON.stringify({
            flag: 0, // meaning to like 
            target_post: parent.className,
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);

        // Replacing like button for unlike button
        let new_like_btn = document.createElement('a');
        new_like_btn.className = 'like';
        new_like_btn.href = '#';
        new_like_btn.innerHTML = `
        <img src="/static/network/un_like.png" alt="ain" height="40rem" width="40rem">
        `;
        
        parent.appendChild(new_like_btn);
        unlike_btn.remove();
    
        // Decrease number of likes by 1
        let unlike_strong_tag = parent.getElementsByClassName(parent.className);
        let n_likes = parseInt(unlike_strong_tag[0].innerHTML);
        unlike_strong_tag[0].innerHTML = n_likes - 1;

        new_like_btn.addEventListener('click', function() {
            like(new_like_btn);
        });
    });
}