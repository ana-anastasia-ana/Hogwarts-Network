document.addEventListener('DOMContentLoaded', function () {
    // Attach click event to all "Like" buttons
    document.querySelectorAll('.like-btn').forEach(function (button) {
        // Determine initial state based on the presence of "liked" class
        const isLiked = button.classList.contains('liked');
        updateHeartColor(button, isLiked);

        button.addEventListener('click', function () {
            const postId = this.dataset.postId;

            // Fetch to the appropriate endpoint
            const endpoint = isLiked ? `/unlike_post/${postId}/` : `/like_post/${postId}/`;

            fetch(endpoint, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                },
            })
                .then(response => response.json())
                .then(data => {
                    // Update like count on the page
                    document.getElementById(`like-count-${postId}`).innerText = data.likes_count;

                    // Toggle the "liked" class based on the new state
                    button.classList.toggle('liked');
                    // Update the heart icon color based on the new state
                    updateHeartColor(button, button.classList.contains('liked'));
                })
                .catch(error => console.error('Error:', error));
        });
    });

    // Function to get CSRF token from cookies
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }

    // Function to update the heart icon color based on the liked state
    function updateHeartColor(button, isLiked) {
        const heartIcon = button.querySelector('i.fa-heart');
        heartIcon.style.color = isLiked ? 'white' : 'red';
    }
});

document.addEventListener('DOMContentLoaded', function() {
    // Attach click event to all "Like" buttons
    document.querySelectorAll('.like-btn').forEach(function(button) {
        button.addEventListener('click', function() {
            console.log('Button clicked!');
        });
    });
});
