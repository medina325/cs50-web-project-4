document.addEventListener("DOMContentLoaded", function() {

    // Check if there are buttons (follow/unfollow) first
    var buttons = document.querySelectorAll('button');
    if (buttons)
    {        
        buttons.forEach((button) => {
            button.addEventListener('click', function() {
                if (button.innerHTML === 'Unfollow')
                    unfollow(button);
                else if (button.innerHTML === 'Follow')
                    follow(button);
            }); 
        });                    
    } 

    // Check if there are edit buttons first
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

function unfollow(btn)
{
    fetch('/followunfollow', {
        method: 'PUT',
        body: JSON.stringify({
            flag: 0, // meaning to unfollow 
            target_user: btn.id, // btn.id contains the id of the user to be unfollowed
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
        let new_follow_btn = document.createElement('button');
        new_follow_btn.className = 'btn btn-success mb-n2';
        new_follow_btn.id = btn.id;
        new_follow_btn.innerHTML = 'Follow';
        
        btn.parentElement.append(new_follow_btn);
        btn.remove();

        new_follow_btn.addEventListener('click', function() {
            follow(new_follow_btn);
        });
    });
}

function follow(btn)
{
    fetch('/followunfollow', {
        method: 'PUT',
        body: JSON.stringify({
            flag: 1, // meaning to follow
            target_user: btn.id, // btn.id contains the id of the user to be followed
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);

        let new_unfollow_btn = document.createElement('button');
        new_unfollow_btn.className = 'btn btn-warning mb-n2';
        new_unfollow_btn.id = btn.id;
        new_unfollow_btn.innerHTML = 'Unfollow';
            
        btn.parentElement.append(new_unfollow_btn);
        btn.remove();

        new_unfollow_btn.addEventListener('click', function() {
            unfollow(new_unfollow_btn);
        });
    });
}