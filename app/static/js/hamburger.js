
/* Hamburger Menu Toggle Script */

document.addEventListener('DOMContentLoaded', function () {
const button = document.getElementById('hamburger-button');
const nav = document.getElementById('hamburger-nav');

button.addEventListener('click', function () {
    nav.style.display = nav.style.display === 'flex' ? 'none' : 'flex';
});

// Optional: click outside to close
document.addEventListener('click', function (e) {
    if (!button.contains(e.target) && !nav.contains(e.target)) {
    nav.style.display = 'none';
    }
});
});
