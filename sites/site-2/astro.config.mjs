import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  site: 'https://jibranpcccc.github.io/workationradar',
  base: process.env.BASE_PATH || '/workationradar/',
  integrations: [tailwind()],
});
