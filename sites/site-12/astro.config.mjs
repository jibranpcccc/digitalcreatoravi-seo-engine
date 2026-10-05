import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  site: 'https://saasunitmath.pages.dev',
  base: '/',
  integrations: [tailwind()],
});
