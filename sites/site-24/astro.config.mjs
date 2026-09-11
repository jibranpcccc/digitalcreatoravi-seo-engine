import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  site: 'https://postgrescale.pages.dev',
  integrations: [tailwind()],
  output: 'static'
});
