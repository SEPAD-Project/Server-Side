document.addEventListener('DOMContentLoaded', function() {
    // Initialize particles.js with reduced interactivity
    particlesJS('particles-js', {
        "particles": {
            "number": {
                "value": 80,
                "density": {
                    "enable": true,
                    "value_area": 800
                }
            },
            "color": {
                "value": ["#00f7ff", "#ff00e4"]
            },
            "shape": {
                "type": "circle",
                "stroke": {
                    "width": 0,
                    "color": "#000000"
                }
            },
            "opacity": {
                "value": 0.5,
                "random": true,
                "anim": {
                    "enable": true,
                    "speed": 1,
                    "opacity_min": 0.1,
                    "sync": false
                }
            },
            "size": {
                "value": 3,
                "random": true,
                "anim": {
                    "enable": true,
                    "speed": 2,
                    "size_min": 0.1,
                    "sync": false
                }
            },
            "line_linked": {
                "enable": true,
                "distance": 150,
                "color": "#ffffff",
                "opacity": 0.2,
                "width": 1
            },
            "move": {
                "enable": true,
                "speed": 1,
                "direction": "none",
                "random": true,
                "straight": false,
                "out_mode": "out",
                "bounce": false
            }
        },
        "interactivity": {
            "detect_on": "canvas",
            "events": {
                "onhover": {
                    "enable": false, // Disabled hover effects
                    "mode": "grab"
                },
                "onclick": {
                    "enable": false, // Disabled click effects
                    "mode": "push"
                },
                "resize": true
            },
            "modes": {
                "grab": {
                    "distance": 140,
                    "line_linked": {
                        "opacity": 0.5
                    }
                },
                "push": {
                    "particles_nb": 4
                }
            }
        },
        "retina_detect": true
    });

    // Form submission (visual only)
    const form = document.querySelector('.login-form');
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        const btn = document.querySelector('.login-btn');
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
        btn.style.background = 'rgba(255, 255, 255, 0.2)';
        btn.style.color = 'white';
        btn.disabled = true;
        
        setTimeout(() => {
            btn.innerHTML = '<i class="fas fa-check"></i><span>AUTHENTICATED</span>';
            btn.style.background = 'rgba(0, 255, 100, 0.2)';
            btn.style.boxShadow = '0 4px 15px rgba(0, 255, 100, 0.3)';
        }, 1500);
    });
});