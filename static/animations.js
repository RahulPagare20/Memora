/* ── animations.js — Premium motion for Memora ── */

// ── PAGE TRANSITION OVERLAY ──
(function() {
    const overlay = document.createElement('div');
    overlay.className = 'page-transition-overlay';
    document.body.appendChild(overlay);

    // Reveal: slide out on load
    overlay.style.animation = 'none';
    overlay.style.transform = 'scaleX(0)';

    document.querySelectorAll('a[href]').forEach(link => {
        const href = link.getAttribute('href');
        if (!href || href.startsWith('#') || href.startsWith('http') || href.startsWith('mailto')) return;
        link.addEventListener('click', e => {
            e.preventDefault();
            overlay.style.transformOrigin = 'left';
            overlay.style.animation = 'pageIn 0.45s cubic-bezier(.76,0,.24,1) forwards';
            setTimeout(() => { window.location.href = href; }, 420);
        });
    });

    window.addEventListener('pageshow', () => {
        overlay.style.transformOrigin = 'right';
        overlay.style.animation = 'pageOut 0.5s cubic-bezier(.76,0,.24,1) forwards';
    });
})();

// ── AURORA BACKGROUND ──
(function() {
    const aurora = document.createElement('div');
    aurora.className = 'aurora-bg';
    aurora.innerHTML = `
        <div class="aurora-layer aurora-1"></div>
        <div class="aurora-layer aurora-2"></div>
        <div class="aurora-layer aurora-3"></div>
        <div class="gradient-blob blob-1"></div>
        <div class="gradient-blob blob-2"></div>
    `;
    document.body.prepend(aurora);
})();

// ── MOUSE GLOW ──
(function() {
    const glow = document.createElement('div');
    glow.className = 'mouse-glow';
    document.body.appendChild(glow);
    let tx = window.innerWidth / 2, ty = window.innerHeight / 2;
    let cx = tx, cy = ty;
    document.addEventListener('mousemove', e => { tx = e.clientX; ty = e.clientY; });
    function tick() {
        cx += (tx - cx) * 0.1;
        cy += (ty - cy) * 0.1;
        glow.style.left = cx + 'px';
        glow.style.top  = cy + 'px';
        requestAnimationFrame(tick);
    }
    tick();
})();

// ── FLOATING PARTICLES ──
(function() {
    const canvas = document.createElement('canvas');
    canvas.className = 'particles-canvas';
    document.body.appendChild(canvas);
    const ctx = canvas.getContext('2d');
    let W, H, particles = [];

    function resize() {
        W = canvas.width  = window.innerWidth;
        H = canvas.height = window.innerHeight;
    }
    resize();
    window.addEventListener('resize', resize);

    const COLORS = [
        `rgba(124,63,228,${0})`,  // placeholder, set per particle
        `rgba(156,111,234,${0})`,
        `rgba(103,48,201,${0})`
    ];
    for (let i = 0; i < 55; i++) {
        particles.push({
            x: Math.random() * window.innerWidth,
            y: Math.random() * window.innerHeight,
            r: Math.random() * 2.5 + 0.5,
            vx: (Math.random() - 0.5) * 0.3,
            vy: (Math.random() - 0.5) * 0.3,
            a: Math.random() * 0.45 + 0.12,
            ci: Math.floor(Math.random() * 3)
        });
    }

    function drawParticles() {
        ctx.clearRect(0, 0, W, H);
        particles.forEach(p => {
            const colors = ['124,63,228', '156,111,234', '103,48,201'];
            ctx.beginPath();
            ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(${colors[p.ci]},${p.a})`;
            ctx.fill();
            p.x += p.vx; p.y += p.vy;
            if (p.x < 0) p.x = W; if (p.x > W) p.x = 0;
            if (p.y < 0) p.y = H; if (p.y > H) p.y = 0;
        });
        requestAnimationFrame(drawParticles);
    }
    drawParticles();
})();

// ── SCROLL REVEAL ──
(function() {
    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('revealed');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.15 });

    document.querySelectorAll('.reveal, .reveal-left, .reveal-right, .stagger-parent').forEach(el => {
        observer.observe(el);
    });
})();

// ── MAGNETIC BUTTONS ──
(function() {
    document.querySelectorAll('.magnetic').forEach(el => {
        el.addEventListener('mousemove', e => {
            const r = el.getBoundingClientRect();
            const dx = e.clientX - (r.left + r.width / 2);
            const dy = e.clientY - (r.top  + r.height / 2);
            el.style.transform = `translate(${dx * 0.25}px, ${dy * 0.25}px)`;
            el.style.setProperty('--mx', ((e.clientX - r.left) / r.width * 100) + '%');
            el.style.setProperty('--my', ((e.clientY - r.top)  / r.height * 100) + '%');
        });
        el.addEventListener('mouseleave', () => {
            el.style.transform = 'translate(0,0)';
        });
    });
})();

// ── ANIMATED COUNTERS ──
function animateCounter(el) {
    const target = parseInt(el.dataset.target, 10);
    const duration = 1800;
    const start = performance.now();
    function update(now) {
        const progress = Math.min((now - start) / duration, 1);
        const ease = 1 - Math.pow(1 - progress, 3);
        el.textContent = Math.round(ease * target) + (el.dataset.suffix || '');
        if (progress < 1) requestAnimationFrame(update);
    }
    requestAnimationFrame(update);
}

const counterObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            animateCounter(entry.target);
            counterObserver.unobserve(entry.target);
        }
    });
}, { threshold: 0.5 });

document.querySelectorAll('[data-counter]').forEach(el => counterObserver.observe(el));



// ── HOVER LIFT — apply to cards automatically ──
document.querySelectorAll('.auth-card, .member-card, .floating-card').forEach(el => {
    el.classList.add('hover-lift');
});

// ── SIDEBAR STAGGER (dashboard) ──
document.querySelectorAll('.sidebar-link').forEach((link, i) => {
    link.style.opacity = '0';
    link.style.transform = 'translateX(-20px)';
    setTimeout(() => {
        link.style.transition = 'opacity 0.4s ease, transform 0.4s ease, all 0.22s cubic-bezier(.22,1,.36,1)';
        link.style.opacity = '';
        link.style.transform = '';
    }, 120 + i * 70);
});

// ── SKELETON LOADERS — replace empty states temporarily ──
(function() {
    const grid = document.getElementById('people-grid');
    if (!grid) return;
    const stored = localStorage.getItem('memora_family');
    if (!stored || JSON.parse(stored).length === 0) {
        grid.innerHTML = Array(3).fill(0).map(() => `
            <div style="background:#ffffff;border:1px solid #e5e5e5;border-radius:14px;padding:28px 20px 22px;text-align:center;">
                <div class="skeleton skeleton-circle" style="width:88px;height:88px;margin:0 auto 16px;"></div>
                <div class="skeleton skeleton-text" style="width:70%;margin:0 auto 8px;"></div>
                <div class="skeleton skeleton-text" style="width:45%;margin:0 auto;height:.8em;"></div>
            </div>
        `).join('');
        setTimeout(() => {
            if (typeof renderMembers === 'function') renderMembers();
        }, 1200);
    }
})();

// ── FORM FIELD FOCUS GLOW ──
document.querySelectorAll('.form-group input, .form-group select').forEach(input => {
    input.addEventListener('focus', () => input.parentElement.style.transform = 'scale(1.01)');
    input.addEventListener('blur',  () => input.parentElement.style.transform = 'scale(1)');
});
document.querySelectorAll('.form-group').forEach(g => {
    g.style.transition = 'transform 0.2s ease';
});

// ── MAGNETIC on primary buttons ──
document.querySelectorAll('.primary-btn, .nav-btn').forEach(btn => btn.classList.add('magnetic'));
