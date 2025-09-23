import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "PST Hibou",
  description: "4A PST",
  themeConfig: {
    nav: [
      { text: 'Guide', link: '/guide/getting-started/what-is-hibou' }
    ],

    sidebar: [
      {
        text: 'Getting Started',
        items: [
          { text: 'What is Hibou', link: '/guide/getting-started/what-is-hibou' },
          { text: 'Acoustics specifications', link: '/guide/getting-started/acoustic' },
          { text: 'Markdown Examples', link: '/guide/getting-started/markdown-examples' },
          { text: 'Credits', link: '/guide/getting-started/credits' },
        ]
      },
      {
        text: 'Hibou Software',
        items: [
          { text: 'Installation', link: '/guide/software/installation'}
        ]
      }
    ],

    socialLinks: [
    ]
  },
  base: '/documentation'
})
