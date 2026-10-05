import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  integrations: [tailwind()],
  site: 'https://devconfighub.pages.dev',
  base: '/',
  build: {
    format: 'directory'
  }
});
