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
                    {
                        text: 'Server installation and configuration', items: [
                            {
                                text: 'Requirements',
                                link: '/guide/installation/server-installation-and-configuration/system-requirement'
                            },
                        ]
                    },
                    {text: 'Client installation', link: ''},
                ]
            },
            {
                text: 'CONFIGURATION',
                items: [
                    {
                        text: 'Environment variables', link: '/guide/configuration/environment-variables'
                    },
                    {text: 'Micro valibration', link: ''},
                ]
            },
            {
                text: 'BUILD FROM SOURCE',
                items: [
                    {text: 'Build Hibou server', link: '/guide/build-from-source/build-Hibou-Server'},
                    {
                        text: 'Dev tips', items: [
                            {
                                text: 'Add devices', items: [
                                    {text: 'PTZ', link: '/guide/build-from-source/dev-tips/devices/add-ptz.md'},
                                    {text: 'ADC', link: '/guide/build-from-source/dev-tips/devices/add-adc.md'},
                                ]
                            }
                        ]
                    },
                ]
            },
            {
                text: 'DEBUG',
                items: [
                    {text: 'Debug Hibou server', link: '/guide/debug/hibou-server'},
                ]
            }
        ],

        socialLinks: []
    },
    base: '/documentation'
})
