import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  integrations: [tailwind()],
  site: 'https://greekvisualizer.pages.dev',
  base: '/',
  build: {
    format: 'directory'
  }
});
