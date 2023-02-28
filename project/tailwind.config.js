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
  },
  plugins: [
    require('flowbite/plugin'),
    require('flowbite-typography')
  ]
}
