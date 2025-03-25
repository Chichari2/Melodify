document.addEventListener("DOMContentLoaded", () => {
    // Smooth section animations on scroll
    const features = document.querySelectorAll(".feature");
    const options = { threshold: 0.2 };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = "1";
                entry.target.style.transform = "translateY(0)";
            }
        });
    }, options);

    features.forEach((feature) => {
        feature.style.opacity = "0";
        feature.style.transform = "translateY(50px)";
        feature.style.transition = "opacity 0.6s ease-out, transform 0.6s ease-out";
        observer.observe(feature);
    });

    // Ripple effect for buttons
    document.querySelectorAll('.ripple').forEach(button => {
        button.addEventListener('click', function(e) {
            const x = e.clientX - e.target.getBoundingClientRect().left;
            const y = e.clientY - e.target.getBoundingClientRect().top;

            const ripple = document.createElement('span');
            ripple.classList.add('ripple-effect');
            ripple.style.left = `${x}px`;
            ripple.style.top = `${y}px`;

            this.appendChild(ripple);

            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
});