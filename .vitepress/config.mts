import {groupIconMdPlugin, groupIconVitePlugin} from 'vitepress-plugin-group-icons'
import buildFromSource from '../guide/build-from-source/routing'
import gettingStarted from '../guide/getting-started/routing'
import installation from '../guide/installation/routing'
import debug from '../guide/debug/routing'
import {defineConfig} from 'vitepress'

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
            })
        ],
    },
    themeConfig: {
        nav: [
            {text: 'Guide', link: '/guide/getting-started/introduction'}
        ],

        sidebar: [
            ...gettingStarted,
            ...installation,
            ...buildFromSource,
            ...debug
        ],

        socialLinks: []
    },
    base: '/documentation'
})
