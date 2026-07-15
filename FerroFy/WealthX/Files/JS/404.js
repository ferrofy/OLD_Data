/* Canvas particle animation and tilt logic extracted from inline script */
const Crypto_Canvas = document.getElementById('Crypto_Canvas');
const Ctx = Crypto_Canvas.getContext('2d');
let Particles = [];

function Resize_Canvas() {
    Crypto_Canvas.width = window.innerWidth;
    Crypto_Canvas.height = window.innerHeight;
}

Resize_Canvas();
window.addEventListener('resize', Resize_Canvas);

for (let i = 0; i < 130; i++) {
    Particles.push({
        x: Math.random() * window.innerWidth,
        y: Math.random() * window.innerHeight,
        z: Math.random() * 2,
        vx: (Math.random() - 0.5) * 0.8,
        vy: (Math.random() - 0.5) * 0.8
    });
}

function Animate() {
    Ctx.clearRect(0, 0, Crypto_Canvas.width, Crypto_Canvas.height);
    for (let P of Particles) {
        P.x += P.vx * P.z;
        P.y += P.vy * P.z;
        if (P.x < 0 || P.x > Crypto_Canvas.width) P.vx *= -1;
        if (P.y < 0 || P.y > Crypto_Canvas.height) P.vy *= -1;
        Ctx.beginPath();
        Ctx.arc(P.x, P.y, P.z * 2, 0, Math.PI * 2);
        Ctx.fillStyle = 'rgba(255,255,255,0.85)';
        Ctx.fill();
    }
    for (let i = 0; i < Particles.length; i++) {
        for (let j = i + 1; j < Particles.length; j++) {
            let Dx = Particles[i].x - Particles[j].x;
            let Dy = Particles[i].y - Particles[j].y;
            let Dist = Math.sqrt(Dx * Dx + Dy * Dy);
            if (Dist < 120) {
                Ctx.beginPath();
                Ctx.moveTo(Particles[i].x, Particles[i].y);
                Ctx.lineTo(Particles[j].x, Particles[j].y);
                Ctx.strokeStyle = 'rgba(255,255,255,' + (1 - Dist / 120) * 0.12 + ')';
                Ctx.stroke();
            }
        }
    }
    requestAnimationFrame(Animate);
}

Animate();

const Tilt_Box = document.getElementById('Tilt_Box');
document.addEventListener('mousemove', (Event) => {
    let X = (Event.clientX / window.innerWidth - 0.5) * 18;
    let Y = (Event.clientY / window.innerHeight - 0.5) * 18;
    if (Tilt_Box) Tilt_Box.style.transform = `rotateY(${X}deg) rotateX(${-Y}deg)`;
});
