import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  site: 'https://featureflagaudit.pages.dev',
  integrations: [tailwind()],
  output: 'static'
});
