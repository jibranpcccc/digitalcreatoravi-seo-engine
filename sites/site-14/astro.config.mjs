import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  integrations: [tailwind()],
  site: 'https://soc2ready.pages.dev',
  base: '/',
  build: {
    format: 'directory'
  }
});
