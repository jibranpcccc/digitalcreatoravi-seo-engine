import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  site: 'https://promptevalhq.pages.dev',
  integrations: [tailwind()],
  output: 'static'
});
