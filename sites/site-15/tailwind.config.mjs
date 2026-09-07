/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        eor: {
          dark: '#090D16',
          card: '#0F172A',
          cardHover: '#1E293B',
          border: '#1E293B',
          emerald: '#10B981',
          green: '#22C55E',
          cyan: '#06B6D4',
          blue: '#3B82F6',
          violet: '#8B5CF6',
          amber: '#F59E0B',
          rose: '#F43F5E'
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
