/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        crm: {
          dark: '#090D16',
          darker: '#05080F',
          card: '#0F172A',
          cardHover: '#1E293B',
          border: '#1E293B',
          borderHover: '#334155',
          emerald: '#10B981',
          emeraldGlow: '#34D399',
          cyan: '#06B6D4',
          amber: '#F59E0B',
          rose: '#F43F5E',
          indigo: '#6366F1'
        }
      },
      fontFamily: {
        mono: ['"JetBrains Mono"', 'Fira Code', 'Menlo', 'Monaco', 'monospace'],
        sans: ['"Plus Jakarta Sans"', 'Inter', 'system-ui', 'sans-serif']
      }
    },
  },
  plugins: [],
}
