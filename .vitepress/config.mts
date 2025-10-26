import {groupIconMdPlugin, groupIconVitePlugin} from 'vitepress-plugin-group-icons'
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
            {text: 'Guide', link: '/guide/getting_started/introduction'}
        ],

        sidebar: [
            {
                text: 'GETTING STARTED',
                items: [
                    {text: 'Introduction', link: '/guide/getting_started/introduction'}
                ]
            },
            {
                text: 'INSTALLATION',
                items: [
                    {text: 'Server installation and configuration', link: ''},
                    {text: 'Client installation', link: ''},
                ]
            },
            {
                text: 'BUILD FROM SOURCE',
                items: [
                    {text: 'Build Hibou Server', link: '/guide/build-from-source/build-Hibou-Server'},
                ]
            },
            {
                text: 'DEBUG',
                items: [
                    {text: 'Debug Hibou Server', link: '/guide/debug/hibou-server'},
                ]
            }
        ],

        socialLinks: []
    },
    base: '/documentation'
})
