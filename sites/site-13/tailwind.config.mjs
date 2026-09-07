/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        obs: {
          dark: '#080C14',
          card: '#0F172A',
          cardHover: '#1E293B',
          border: '#1E293B',
          cyan: '#06B6D4',
          cyanGlow: '#22D3EE',
          emerald: '#10B981',
          amber: '#F59E0B',
          purple: '#8B5CF6'
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
