import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  site: 'https://nomadpassportindex.pages.dev',
  integrations: [tailwind()],
  output: 'static'
});
