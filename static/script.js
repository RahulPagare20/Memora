// Navbar scroll effect
const navbar = document.querySelector('.navbar');
if (navbar) {
    window.addEventListener('scroll', () => {
        navbar.style.background = window.scrollY > 50
            ? 'rgba(245,239,230,0.98)'
            : 'rgba(245,239,230,0.9)';
    });
}

// Staggered float delays on cards
document.querySelectorAll('.floating-card').forEach((card, i) => {
    card.style.animationDelay = `${i * 1.2}s`;
});

// Fade-in hero content on load
const heroContent = document.querySelector('.hero-content');
if (heroContent) {
    heroContent.style.opacity = '0';
    heroContent.style.transform = 'translateY(30px)';
    heroContent.style.transition = 'opacity 0.9s ease, transform 0.9s ease';
    window.addEventListener('load', () => {
        setTimeout(() => {
            heroContent.style.opacity = '1';
            heroContent.style.transform = 'translateY(0)';
        }, 100);
    });
}

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

// Toggle password visibility
function togglePassword() {
    const input = document.getElementById('password');
    const btn = document.querySelector('.eye-btn');
    if (!input) return;
    const show = input.type === 'password';
    input.type = show ? 'text' : 'password';
    btn.textContent = show ? '🚫' : '👁';
}

// Country codes
const COUNTRY_CODES = [
    { code: '+91', name: 'India' },
    { code: '+1', name: 'USA/Canada' },
    { code: '+44', name: 'UK' },
    { code: '+61', name: 'Australia' },
    { code: '+81', name: 'Japan' },
    { code: '+49', name: 'Germany' },
    { code: '+33', name: 'France' },
    { code: '+39', name: 'Italy' },
    { code: '+34', name: 'Spain' },
    { code: '+55', name: 'Brazil' },
    { code: '+52', name: 'Mexico' },
    { code: '+86', name: 'China' },
    { code: '+82', name: 'South Korea' },
    { code: '+65', name: 'Singapore' },
    { code: '+971', name: 'UAE' },
    { code: '+966', name: 'Saudi Arabia' },
    { code: '+27', name: 'South Africa' },
    { code: '+234', name: 'Nigeria' },
    { code: '+254', name: 'Kenya' },
    { code: '+92', name: 'Pakistan' },
    { code: '+880', name: 'Bangladesh' },
    { code: '+94', name: 'Sri Lanka' },
    { code: '+977', name: 'Nepal' },
    { code: '+64', name: 'New Zealand' },
    { code: '+31', name: 'Netherlands' },
    { code: '+46', name: 'Sweden' },
    { code: '+47', name: 'Norway' },
    { code: '+45', name: 'Denmark' },
    { code: '+358', name: 'Finland' },
    { code: '+41', name: 'Switzerland' },
    { code: '+43', name: 'Austria' },
    { code: '+32', name: 'Belgium' },
    { code: '+351', name: 'Portugal' },
    { code: '+48', name: 'Poland' },
    { code: '+7', name: 'Russia' },
    { code: '+90', name: 'Turkey' },
    { code: '+20', name: 'Egypt' },
    { code: '+62', name: 'Indonesia' },
    { code: '+63', name: 'Philippines' },
    { code: '+60', name: 'Malaysia' },
    { code: '+66', name: 'Thailand' },
    { code: '+84', name: 'Vietnam' },
];

function populateCountryCodes() {
    document.querySelectorAll('.country-code').forEach(select => {
        COUNTRY_CODES.forEach(c => {
            const opt = document.createElement('option');
            opt.value = c.code;
            opt.textContent = `${c.name} (${c.code})`;
            select.appendChild(opt);
        });
    });
}

populateCountryCodes();
