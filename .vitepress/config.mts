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
import fs from 'node:fs'
import { defineConfig } from 'vitepress'
import { vitepressMermaidPreview } from 'vitepress-mermaid-preview'


const docsSidebars = buildDocsSidebars(fileURLToPath(new URL('../docs', import.meta.url)))
const docsRoot = fileURLToPath(new URL('../docs', import.meta.url))

function buildDocsFooterLinks(): { text: string; collapsed: boolean; items: { text: string; link: string }[] }[] {
    const projects = fs.readdirSync(docsRoot, {withFileTypes: true})
        .filter((entry) => entry.isDirectory() && !entry.name.startsWith('.'))
        .map((entry) => entry.name)
        .sort((a, b) => a.localeCompare(b))

    if (!projects.length) {
        return []
    }

    return [
        {
            text: 'More',
            collapsed: true,
            items: projects.map((project) => ({
                text: project.replace(/[_-]+/g, ' ').replace(/\b\w/g, (match) => match.toUpperCase()),
                link: `/docs/${project}/`,
            })),
        },
    ]
}


// https://vitepress.dev/reference/site-config
export default defineConfig({
    title: 'Hibou',
    description: 'Detect, Locate, Indentify drones threat',
    markdown: {
        config: (md) => {
            vitepressMermaidPreview(md.use(groupIconMdPlugin), { showToolbar: true })
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
        search: {
            provider: 'local',
        },
        sidebar: {
            '/guide/': [
                ...gettingStarted,
                ...installation,
                ...buildFromSource,
                ...debug,
                ...ai,
                ...drone,
                ...buildDocsFooterLinks(),
            ],
            ...docsSidebars,
        },

        socialLinks: []
    },
    base: '/documentation'
})
