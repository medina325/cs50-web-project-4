document.addEventListener('DOMContentLoaded', function() {

    // Like and unlike button handlers
    document.querySelectorAll('.like').forEach(like_button => {
        like_button.onclick = () => like(like_button);
    });

    document.querySelectorAll('.unlike').forEach(unlike_button => {
        unlike_button.onclick = () => unlike(unlike_button);
    });
});