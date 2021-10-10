document.addEventListener('DOMContentLoaded', function() {
    posts = Array.from(document.querySelectorAll('.post'));
    posts.forEach(post => {
        edit_button = post.querySelector('.edit-button');
        if (edit_button !== null) {
            edit_button.addEventListener('click', () => edit(post));
        }
        like_icon = post.querySelector('.like-icon');
        if (like_icon !== null) {
            like_icon.addEventListener('click', () => like(post));
            updateLikeView(post);
        }
    });
});

function edit(post) {
    if (post != null)
    {
        edit_button = post.querySelector('.edit-button');
        edit_button.style.display = 'none';
        content = post.querySelector('.post-content');
        content.style.display = 'none';

        save_button = document.createElement('button');
        save_button.classList.add('save-button');
        save_button.innerHTML = 'Save';
        save_button.addEventListener('click', () => save(post));

        text_area = document.createElement('textarea');
        text_area.classList.add('edit-content');
        text_area.value = content.textContent;
        
        post.insertBefore(text_area, content);
        post.insertBefore(save_button, edit_button);
    }
}

function save(post) {
    text_area = post.querySelector('.edit-content');
    post_content = post.querySelector('.post-content');
    post_content.textContent = text_area.value;

    fetch('/edit', {
        method: 'PUT',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            content: post_content.textContent,
            id: post.dataset.id,
        })
    })
    .then(() => removeEditView(post));
}

function like(post) {
    fetch('/like', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            id: post.dataset.id,
        })
    })
    .then(() => updateLikeView(post));
}

function updateLikeView(post) {
    fetch(`/post_likes/${post.dataset.id}`)
    .then(response => response.json())
    .then(data => {
        likes = post.querySelector('.post-likes');
        like_icon = post.querySelector('.like-icon');
        likes.textContent = `${data.likes} likes`;
        if (data.user_liked) {
            like_icon.src = "/static/network/like-icon.png"
        }
        else {
            like_icon.src = "/static/network/like-icon-empty.png"
        }
    })
}

function removeEditView(post) {
    post.querySelector('.edit-content').remove()
    post.querySelector('.save-button').remove()
    post.querySelector('.post-content').style.display = 'block';
    post.querySelector('.edit-button').style.display = 'inline';
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}