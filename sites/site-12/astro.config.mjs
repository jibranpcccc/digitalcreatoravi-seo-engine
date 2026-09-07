import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  site: 'https://site-12-taupe.vercel.app',
  base: '/',
  integrations: [tailwind()],
});
