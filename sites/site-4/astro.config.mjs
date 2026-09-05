import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  integrations: [tailwind()],
  site: 'https://indiestackaudit.pages.dev',
  base: '/',
  build: {
    format: 'directory'
  }
});
