document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('theme-toggle');
    const html = document.documentElement;

    // Get stored theme or use preferred color scheme
    const storedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

    // Set initial theme
    const initialTheme = storedTheme || (prefersDark ? 'dark' : 'light');
    html.setAttribute('data-theme', initialTheme);

    // Listen for system theme changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
        if (!storedTheme) {
            const newTheme = e.matches ? 'dark' : 'light';
            html.classList.add('theme-transition');
            html.setAttribute('data-theme', newTheme);
            setTimeout(() => {
                html.classList.remove('theme-transition');
            }, 300);
        }
    });

    // Toggle theme on button click
    themeToggle.addEventListener('click', () => {
        const currentTheme = html.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

        // Add transition class
        html.classList.add('theme-transition');
        setTimeout(() => {
            html.classList.remove('theme-transition');
        }, 300);

        // Set new theme
        html.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
    });
});