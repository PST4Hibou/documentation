// .vitepress/theme/index.ts
import type { Theme } from 'vitepress'
import DefaultTheme from 'vitepress/theme'
import { initComponent } from 'vitepress-mermaid-preview/component'
import 'vitepress-mermaid-preview/dist/index.css'
import 'virtual:group-icons.css'
import 'uno.css'
import './style.css'

export default {
    extends: DefaultTheme,
    enhanceApp({ app }) {
        initComponent(app)
    },
} satisfies Theme
