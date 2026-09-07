import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  site: 'https://site-9-inky.vercel.app',
  integrations: [tailwind()],
  output: 'static'
});
