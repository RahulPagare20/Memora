// Navbar scroll effect
const navbar = document.querySelector('.navbar');
window.addEventListener('scroll', () => {
    navbar.style.background = window.scrollY > 50
        ? 'rgba(10,10,15,0.95)'
        : 'rgba(10,10,15,0.8)';
});

// Staggered float delays on cards
document.querySelectorAll('.floating-card').forEach((card, i) => {
    card.style.animationDelay = `${i * 1.2}s`;
});

// Fade-in hero content on load
const heroContent = document.querySelector('.hero-content');
heroContent.style.opacity = '0';
heroContent.style.transform = 'translateY(30px)';
heroContent.style.transition = 'opacity 0.9s ease, transform 0.9s ease';

window.addEventListener('load', () => {
    setTimeout(() => {
        heroContent.style.opacity = '1';
        heroContent.style.transform = 'translateY(0)';
    }, 100);
});

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', e => {
        const target = document.querySelector(anchor.getAttribute('href'));
        if (target) {
            e.preventDefault();
            target.scrollIntoView({ behavior: 'smooth' });
        }
    });
});
