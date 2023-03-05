// Get references to the elements we need
const html = document.documentElement;
const themeToggleBtn = document.getElementById('theme-toggle');
const themeToggleDarkIcon = document.getElementById('theme-toggle-dark-icon');
const themeToggleLightIcon = document.getElementById('theme-toggle-light-icon');

// Function to toggle the theme
function toggleTheme() {
  html.classList.toggle('dark');
  const isDark = html.classList.contains('dark');
  localStorage.setItem('color-theme', isDark ? 'dark' : 'light');
  themeToggleDarkIcon.classList.toggle('hidden', isDark);
  themeToggleLightIcon.classList.toggle('hidden', !isDark);
}

// Set the initial theme based on local storage or browser settings
if (localStorage.getItem('color-theme') === 'dark' || (!localStorage.getItem('color-theme') && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
  toggleTheme();
}

// Add click event listener to theme toggle button
themeToggleBtn.addEventListener('click', toggleTheme);