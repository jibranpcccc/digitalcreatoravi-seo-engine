import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  site: 'https://nomadpassportindex.netlify.app',
  integrations: [tailwind()],
  output: 'static'
});
