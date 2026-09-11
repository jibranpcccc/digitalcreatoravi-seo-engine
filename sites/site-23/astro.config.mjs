import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  site: 'https://opentelemetrylab.pages.dev',
  integrations: [tailwind()],
  output: 'static'
});
