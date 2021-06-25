// Edit post

const editInput = document.querySelectorAll('.posts');

editInput.forEach(item => {
    item.addEventListener('click', e => {
        const btn = e.target;

        // When you click Edit...
        if (btn.classList.contains('btn-edit')) {
            const input = btn.parentElement.parentElement.nextElementSibling;

            // Show Save button
            btn.classList.add('btn-hide');
            btn.nextElementSibling.classList.remove('btn-hide');
            
            input.innerHTML = `<input value="${input.innerText}">`
        }
        
        // When you click Save...
        if (btn.classList.contains('btn-save')) {
            const newInput = btn.parentElement.parentElement.nextElementSibling;

            // Store the new edited post in newInputValue variable
            const newInputValue = btn.parentElement.parentElement.nextElementSibling.firstElementChild.value;

            // Show Edit button
            btn.classList.add('btn-hide');
            btn.previousElementSibling.classList.remove('btn-hide');
            
            // Add the new edited post to front-end
            newInput.innerHTML = `<p>${newInputValue}</p>`;
            
            // Create a CSRF token
            const cookie = document.cookie
            const csrfToken = cookie.substring(cookie.indexOf('=') + 1)

            // Send a PUT request to change the post in database
            fetch(`../edit_post/${newInput.dataset.postId}`, {
                method: 'PUT',
                headers: {
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({
                    body: newInputValue
                })
            })
        }
    })
})


// Add/Remove Likes

const likeBtn = document.querySelectorAll('.like-btn');

likeBtn.forEach(item => {
    item.addEventListener('click', e => {
        // Create a CSRF token
        const cookie = document.cookie
        const csrfToken = cookie.substring(cookie.indexOf('=') + 1)
        // Update the like count
        fetch(`/like/${e.target.id}/likes`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken
              }
        })
        // Fetch the actual likes number from database and update without refreshing the page
        .then(() => {
            fetch(`/like/${e.target.id}/likes-get`)
            .then(response => response.json())
            .then(post => {
                // Update the like counter in front-end
                e.target.nextElementSibling.innerHTML = post.total_likes;
                // Update the heart icon in front-end
                if (post.total_likes == 0) {
                    e.target.classList.remove('fas');
                    e.target.classList.add('far');
                }
                if (post.total_likes > 0) {
                    e.target.classList.remove('far');
                    e.target.classList.add('fas');
                }
            })
        })
    })
});


// Follow/Unfollow

const profile = document.querySelector('.profile');

profile.addEventListener('click', e => {
    const btn = e.target;
    // Select the follower counter
    const follower = document.querySelector('.follower');
    // Get the user's id who wish to follow/unfollow
    const userId = btn.parentElement.dataset.userId;
    // Value of the counter
    const int = parseInt(follower.innerHTML)

    // Create a CSRF token
    const cookie = document.cookie
    const csrfToken = cookie.substring(cookie.indexOf('=') + 1)

    // When you click Follow...
    if (btn.classList.contains('follow')) {
        // Show Unfollow button
        btn.previousElementSibling.classList.remove('btn-hide');
        btn.classList.add('btn-hide');
        // Update the follower counter at front-end
        follower.innerHTML = int+1
    }

    // When you click Unfollow...
    if (btn.classList.contains('unfollow')) {  
        // Show Follow button
        btn.nextElementSibling.classList.remove('btn-hide');
        btn.classList.add('btn-hide');
        // Update the follower counter at front-end
        follower.innerHTML = int-1
    }

    // Send a POST request to database to update followers
    fetch(`/follow/${userId}/follow`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken
        }
    })
});

