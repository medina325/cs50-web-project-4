document.addEventListener("DOMContentLoaded", function() {
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