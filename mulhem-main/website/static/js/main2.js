import confetti from "https://cdn.skypack.dev/canvas-confetti";

function bigConfetti() {
    for (let i = 0; i < 50; i++) { // قلل عدد الحلقات
        confetti({
            particleCount: 20, // قلل عدد الجسيمات في كل إطلاق
            startVelocity: Math.random() * 50, // سرعة البداية
            spread: Math.random() * 10 + 60, // تقليل التشتت
            angle: 90, // اتجاه من الأعلى إلى الأسفل
            gravity: Math.random() * 0.5 + 1.5, // زيادة الجاذبية لتسريع الهبوط
            scalar: Math.random() * 1.5, // أحجام عشوائية صغيرة
            colors: ['#ff0000', '#00ff00', '#0000ff', '#ffff00', '#ff00ff'], // ألوان زاهية
            origin: {
                x: Math.random(), // موقع أفقي عشوائي
                y: 0 // ابدأ من الأعلى
            }
        });
    }
     // Play Clap Sound
     const audio = document.getElementById('clap-sound');
     audio.currentTime = 0; // Reset audio to the start
     audio.play();
}

// Make Function Global
window.bigConfetti = bigConfetti;
// Copyright (c) 2024 by Chris Coyier  (https://codepen.io/chriscoyier/pen/vYKvEQx)


















