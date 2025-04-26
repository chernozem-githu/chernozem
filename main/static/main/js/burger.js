function toggleMenu() {
    const aside = document.querySelector('aside');
    aside.classList.toggle('open');
}

// Закрытие меню при клике на ссылку
document.querySelectorAll('aside a').forEach(link => {
    link.addEventListener('click', () => {
        const aside = document.querySelector('aside');
        aside.classList.remove('open');
    });
});
