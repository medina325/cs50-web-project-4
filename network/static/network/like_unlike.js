function like(like_btn) {
    let parent = like_btn.parentNode;

    fetch('/likeunlike', {
        method: 'PUT',
        body: JSON.stringify({
            flag: 1, // means to like 
            target_post: parent.className,
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);

        // Replacing like button for unlike button
        let new_unlike_button = document.createElement('a');
        new_unlike_button.className = 'unlike';
        new_unlike_button.href = '#!';
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
            flag: 0, // means to like 
            target_post: parent.className,
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);

        // Replacing like button for unlike button
        let new_like_btn = document.createElement('a');
        new_like_btn.className = 'like';
        new_like_btn.href = '#!';
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