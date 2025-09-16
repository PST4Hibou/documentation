import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: "PST Hibou",
  description: "4A PST",
  themeConfig: {
    nav: [
      { text: 'Guide', link: '/guide/what-is-hibou' }
    ],

    sidebar: [
      {
        text: 'Examples',
        items: [
          { text: 'What is Hibou', link: '/guide/what-is-hibou' },
          { text: 'Acoustics specifications', link: '/guide/acoustic' },
          { text: 'Markdown Examples', link: '/guide/markdown-examples' },
          { text: 'Credits', link: '/guide/credits' },
        ]
      }
    ],

    socialLinks: [
    ]
  },
  base: '/documentation'
})
