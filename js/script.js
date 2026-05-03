let currentLang = localStorage.getItem('selectedLanguage') || 'en';

function applyLanguage() {
  // Update document lang attribute
  document.documentElement.lang = currentLang;
  
  // Update all translatable elements (class="tl")
  document.querySelectorAll('.tl').forEach(el => {
    const translatedText = el.getAttribute(`data-${currentLang}`);
    if(translatedText) {
      el.textContent = translatedText;
    }
  });
  
  // Update active state on the toggle button
  const jaEl = document.getElementById('lang-ja');
  const enEl = document.getElementById('lang-en');
  
  if(jaEl && enEl) {
    if(currentLang === 'ja') {
      jaEl.classList.add('active');
      enEl.classList.remove('active');
    } else {
      jaEl.classList.remove('active');
      enEl.classList.add('active');
    }
  }
}

function toggleLanguage() {
  // Switch language state
  currentLang = currentLang === 'ja' ? 'en' : 'ja';
  localStorage.setItem('selectedLanguage', currentLang);
  
  applyLanguage();
}

// Wave Background Animation
class Wave {
  constructor(canvas, color, speed, amplitude, frequency, yOffset, strokeColor = null, lineWidth = 0) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.color = color;
    this.speed = speed;
    this.amplitude = amplitude;
    this.frequency = frequency;
    this.yOffset = yOffset;
    this.strokeColor = strokeColor;
    this.lineWidth = lineWidth;
    this.phase = 0;
  }

  draw() {
    this.ctx.beginPath();
    this.ctx.moveTo(0, this.canvas.height);
    
    for (let x = 0; x <= this.canvas.width; x += 10) {
      let y = Math.sin((x * this.frequency) + this.phase) * this.amplitude;
      this.ctx.lineTo(x, this.canvas.height * this.yOffset - y);
    }
    
    this.ctx.lineTo(this.canvas.width, this.canvas.height);
    this.ctx.lineTo(0, this.canvas.height);
    this.ctx.closePath();
    
    if (this.color) {
      this.ctx.fillStyle = this.color;
      this.ctx.fill();
    }
    
    if (this.strokeColor && this.lineWidth > 0) {
      this.ctx.beginPath();
      for (let x = 0; x <= this.canvas.width; x += 10) {
        let y = Math.sin((x * this.frequency) + this.phase) * this.amplitude;
        if (x === 0) {
          this.ctx.moveTo(x, this.canvas.height * this.yOffset - y);
        } else {
          this.ctx.lineTo(x, this.canvas.height * this.yOffset - y);
        }
      }
      this.ctx.strokeStyle = this.strokeColor;
      this.ctx.lineWidth = this.lineWidth;
      this.ctx.stroke();
    }
    
    this.phase += this.speed;
  }
}

function initWaveAnimation() {
  const canvas = document.getElementById('waveCanvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  
  let waves = [];
  
  function resize() {
    canvas.width = canvas.parentElement.offsetWidth;
    canvas.height = canvas.parentElement.offsetHeight;
    
    waves = [
      new Wave(canvas, 'rgba(48, 54, 61, 0.6)', 0.012, canvas.height * 0.15, 0.002, 0.75), // Dark Grayish
      new Wave(canvas, 'rgba(47, 129, 247, 0.25)', 0.015, canvas.height * 0.18, 0.003, 0.7), // Accent Blue
      new Wave(canvas, 'rgba(139, 148, 158, 0.3)', 0.02, canvas.height * 0.12, 0.0025, 0.85), // Light Gray
      new Wave(canvas, 'rgba(230, 237, 243, 0.05)', 0.025, canvas.height * 0.2, 0.0015, 0.8, 'rgba(255, 255, 255, 0.25)', 2) // White/Light with stroke
    ];
  }
  
  window.addEventListener('resize', resize);
  resize();
  
  function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    waves.forEach(wave => wave.draw());
    requestAnimationFrame(animate);
  }
  
  animate();
}

document.addEventListener('DOMContentLoaded', () => {
  applyLanguage();
  initWaveAnimation();
});
