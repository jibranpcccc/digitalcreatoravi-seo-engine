import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';

function rehypeBasePrefix() {
  const basePath = process.env.BASE_PATH || '/';
  const base = basePath.endsWith('/') ? basePath : basePath + '/';
  if (base === '/') return () => {};
  
  return (tree) => {
    function visit(node) {
      if (node.type === 'element') {
        if (node.tagName === 'img' && typeof node.properties?.src === 'string' && node.properties.src.startsWith('/')) {
          if (!node.properties.src.startsWith(base)) {
            node.properties.src = base + node.properties.src.replace(/^\//, '');
          }
        }
        if (node.tagName === 'a' && typeof node.properties?.href === 'string' && node.properties.href.startsWith('/')) {
          if (!node.properties.href.startsWith(base) && !node.properties.href.startsWith('//')) {
            node.properties.href = base + node.properties.href.replace(/^\//, '');
          }
        }
      }
      if (node.children) {
        for (const child of node.children) {
          visit(child);
        }
      }
    }
    visit(tree);
  };
}

export default defineConfig({
  integrations: [tailwind()],
  site: 'https://jibranpcccc.github.io',
  base: process.env.BASE_PATH || '/',
  markdown: {
    rehypePlugins: [rehypeBasePrefix],
  },
});
