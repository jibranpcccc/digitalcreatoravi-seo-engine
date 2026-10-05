import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  site: 'https://founderrunway.pages.dev',
  integrations: [tailwind()],
  output: 'static'
});
