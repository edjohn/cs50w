document.addEventListener('DOMContentLoaded', () => {
    updateNavbar();
});
document.addEventListener('scroll', updateNavbar);

function updateNavbar() {
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {
        displayNavbar();
    }
    else {
        hideNavbar();
    }
}

function displayNavbar() { 
    bottomNavbar = document.querySelector('#bottom-navbar');
    bottomNavbar.style.display = 'flex';
    bottomNavbar.style.animation = 'fadeIn 0.25s linear 0s 1 normal forwards running';
}

function hideNavbar() {
    bottomNavbar = document.querySelector('#bottom-navbar');
    bottomNavbar.style.display = 'flex';
    bottomNavbar.style.animation = 'fadeOut 0.25s linear 0s 1 normal forwards running';
}
