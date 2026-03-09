import {groupIconMdPlugin, groupIconVitePlugin} from 'vitepress-plugin-group-icons'
import buildFromSource from '../guide/build-from-source/routing'
import gettingStarted from '../guide/getting-started/routing'
import installation from '../guide/installation/routing'
import debug from '../guide/debug/routing'
import ai from '../guide/ai/routing'
import drone from '../guide/drone/routing'
import {defineConfig} from 'vitepress'
import { fileURLToPath } from 'node:url'
import { buildDocsSidebars } from './sidebar/docs'
import UnoCSS from 'unocss/vite'

const docsSidebars = buildDocsSidebars(fileURLToPath(new URL('../docs', import.meta.url)))

// https://vitepress.dev/reference/site-config
export default defineConfig({
    title: 'Hibou',
    description: 'Detect, Locate, Indentify drones threat',
    markdown: {
        config(md) {
            md.use(groupIconMdPlugin)
        },
    },
    vite: {
        plugins: [
            groupIconVitePlugin({
                customIcon: {
                    'ubuntu': 'logos:ubuntu',
                    'fedora': 'logos:fedora'
                },
            }),
            UnoCSS()
        ],
    },
    themeConfig: {
        nav: [
            {text: 'Guide', link: '/guide/getting-started/introduction'}
        ],

        sidebar: {
            '/guide/': [
                ...gettingStarted,
                ...installation,
                ...buildFromSource,
                ...debug,
                ...ai,
                ...drone,
            ],
            ...docsSidebars,
        },

        socialLinks: []
    },
    base: '/documentation'
})
