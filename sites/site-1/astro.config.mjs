import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  integrations: [tailwind()],
  site: 'https://jibranpcccc.github.io',
  base: process.env.BASE_PATH || '/',
});
