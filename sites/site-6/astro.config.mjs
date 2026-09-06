import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  integrations: [tailwind()],
  site: 'https://nomadtreaty.vercel.app',
  base: '/',
  build: {
    format: 'directory'
  }
});
