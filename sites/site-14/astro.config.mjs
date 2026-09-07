import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  integrations: [tailwind()],
  site: 'https://site-14-sable.vercel.app',
  base: '/',
  build: {
    format: 'directory'
  }
});
