/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        agent: {
          50: '#ecfdf5',
          500: '#10b981',
          600: '#059669',
          900: '#064e3b',
          950: '#022c22'
        }
      }
    },
  },
  plugins: [],
};
