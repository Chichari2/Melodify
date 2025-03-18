// main.js

document.addEventListener("DOMContentLoaded", () => {
    const themeToggleButton = document.getElementById('theme-toggle').querySelector('button');

    const setTheme = (theme) => {
        document.documentElement.setAttribute("data-theme", theme);
        localStorage.setItem("theme", theme);
        themeToggleButton.innerText = theme === "dark" ? "☀️" : "🌙";  // Update the button text
    };

    // Load theme from localStorage
    const currentTheme = localStorage.getItem("theme") || "light";
    setTheme(currentTheme);

    themeToggleButton.addEventListener("click", () => {
        const newTheme = document.documentElement.getAttribute("data-theme") === "dark" ? "light" : "dark";
        setTheme(newTheme);
    });

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
});
