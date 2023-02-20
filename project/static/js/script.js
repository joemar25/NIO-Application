// =============================== Imports are found inside index.js ================================

// ======================================== END of Imports ==========================================

// ============================================ Dark Mode ===========================================

// On page load or when changing themes, best to add inline in `head` to avoid FOUC
if (localStorage.getItem('color-theme') === 'dark' || (!('color-theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    document.documentElement.classList.add('dark');
} else {
    document.documentElement.classList.remove('dark')
}

var themeToggleDarkIcon = document.getElementById('theme-toggle-dark-icon');
var themeToggleLightIcon = document.getElementById('theme-toggle-light-icon');

// Change the icons inside the button based on previous settings
if (localStorage.getItem('color-theme') === 'dark' || (!('color-theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    themeToggleLightIcon.classList.remove('hidden');
} else {
    themeToggleDarkIcon.classList.remove('hidden');
}

var themeToggleBtn = document.getElementById('theme-toggle');

themeToggleBtn.addEventListener('click', function () {

    // toggle icons inside button
    themeToggleDarkIcon.classList.toggle('hidden');
    themeToggleLightIcon.classList.toggle('hidden');

    // if set via local storage previously
    if (localStorage.getItem('color-theme')) {
        if (localStorage.getItem('color-theme') === 'light') {
            document.documentElement.classList.add('dark');
            localStorage.setItem('color-theme', 'dark');
        } else {
            document.documentElement.classList.remove('dark');
            localStorage.setItem('color-theme', 'light');
        }

        // if NOT set via local storage previously
    } else {
        if (document.documentElement.classList.contains('dark')) {
            document.documentElement.classList.remove('dark');
            localStorage.setItem('color-theme', 'light');
        } else {
            document.documentElement.classList.add('dark');
            localStorage.setItem('color-theme', 'dark');
        }
    }

});

// bar graph backend

const labelsBarChart = [
  "Feedback 1",
  "Feedback 2",
  "Feedback 3",
  "Feedback 4",
];
const dataBarChart = {
  labels: labelsBarChart,
  datasets: [
    {
      label: "Speech Rating",
      backgroundColor: "hsl(120, 60%, 50%)",
      borderColor: "hsl(252, 82.9%, 67.8%)",
      data: [85,73,90,88,100],
    },
  ],
};

const configBarChart = {
  type: "bar",
  data: dataBarChart,
  options: {},
};

var chartBar = new Chart(
  document.getElementById("chartBar"),
  configBarChart
);

// ============================================== End ===============================================



