/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        indie: {
          50: '#faf5ff',
          500: '#a855f7',
          600: '#9333ea',
          900: '#581c87',
          950: '#2e1065'
        }
      }
    },
  },
  plugins: [],
};
