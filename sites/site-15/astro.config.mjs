import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  integrations: [tailwind()],
  site: 'https://eorcalculator.pages.dev',
  base: '/',
  build: {
    format: 'directory'
  }
});
