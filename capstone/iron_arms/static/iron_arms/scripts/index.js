document.addEventListener('DOMContentLoaded', function() {
    applyAnimations()
});

function applyAnimations() {
    nodes = document.querySelector('section').children;
    delay = 0
    for (i = 0; i < nodes.length; i++) {
        nodeStyle = nodes[i].style;
        nodeStyle.opacity = 0;
        nodeStyle.animation = `fadeIn 1s linear ${delay}s 1 normal forwards running`;
        delay += 1;
    }
}