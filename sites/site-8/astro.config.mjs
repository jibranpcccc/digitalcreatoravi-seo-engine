import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  site: 'https://localdocprivacy.pages.dev',
  integrations: [tailwind()],
  output: 'static'
});
