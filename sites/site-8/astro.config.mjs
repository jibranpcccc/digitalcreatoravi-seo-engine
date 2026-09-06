import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  site: 'https://localdocprivacy.netlify.app',
  integrations: [tailwind()],
  output: 'static'
});
