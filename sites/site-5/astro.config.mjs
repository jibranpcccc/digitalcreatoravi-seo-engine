import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  integrations: [tailwind()],
  site: 'https://vectorbench-hq.netlify.app',
  base: '/',
  build: {
    format: 'directory'
  }
});
