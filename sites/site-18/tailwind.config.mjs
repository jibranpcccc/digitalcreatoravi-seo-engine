/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        ci: {
          bg: '#090D16',
          card: '#0F172A',
          cardHover: '#1E293B',
          border: '#1E293B',
          cyan: '#06B6D4',
          emerald: '#10B981',
          amber: '#F59E0B',
          purple: '#8B5CF6',
          blue: '#3B82F6',
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
