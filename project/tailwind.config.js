/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/src/**/*.js",
    "./node_modules/flowbite/**/*.js",
  ],

  darkMode: 'class',
  theme: {
    container: {
      center: true,
      top: '2rem',
    },
    extend: {
      typography: (theme) => ({
        DEFAULT: {
          css: {
            // Set the base font size to 18px
            fontSize: '18px',
            // Set the line height to 1.5
            lineHeight: '1.5',
          },
        },
      }),
    },
  },
  plugins: [
    require('flowbite/plugin'),
    require('flowbite-typography')
  ]
}
