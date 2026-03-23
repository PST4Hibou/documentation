import fs from 'node:fs'
import path from 'node:path'
import type { DefaultTheme } from 'vitepress'

const INDEX_FILE = 'index.md'

function formatTitle(name: string): string {
    const cleaned = name.replace(/\.[^/.]+$/, '').replace(/[_-]+/g, ' ')
    return cleaned.replace(/\b\w/g, (match) => match.toUpperCase())
}

function toLink(project: string, relNoExt: string, isIndex: boolean): string {
    if (isIndex) {
        return relNoExt ? `/docs/${relNoExt}/` : `/docs/${project}/`
    }
    return `/docs/${relNoExt}`
}

function readDirItems(
    docsRoot: string,
    project: string,
    dirRel: string,
    depth: number,
): DefaultTheme.SidebarItem[] {
    const fullDir = path.join(docsRoot, dirRel)
    const entries = fs.readdirSync(fullDir, {withFileTypes: true})
        .filter((entry) => !entry.name.startsWith('.'))

    const files = entries
        .filter((entry) => entry.isFile() && entry.name.endsWith('.md'))
        .map((entry) => entry.name)

    const dirs = entries
        .filter((entry) => entry.isDirectory())
        .map((entry) => entry.name)

    const dirNameSet = new Set(dirs)
    const fileBaseNameToFile = new Map(
        files.map((name) => [name.replace(/\.md$/, ''), name]),
    )

    const items: DefaultTheme.SidebarItem[] = []

    if (files.includes(INDEX_FILE)) {
        items.push({
            text: 'Overview',
            link: toLink(project, dirRel.replace(/\\/g, '/'), true),
        })
    }

    files
        .filter((name) => name !== INDEX_FILE)
        .filter((name) => !dirNameSet.has(name.replace(/\.md$/, '')))
        .sort((a, b) => a.localeCompare(b))
        .forEach((name) => {
            const relNoExt = path.join(dirRel, name.replace(/\.md$/, '')).replace(/\\/g, '/')
            items.push({
                text: formatTitle(name),
                link: toLink(project, relNoExt, false),
            })
        })

    dirs
        .sort((a, b) => a.localeCompare(b))
        .forEach((dirName) => {
            const childRel = path.join(dirRel, dirName)
            const childItems = readDirItems(docsRoot, project, childRel, depth + 1)
            if (!childItems.length) {
                return
            }

            const dirIndex = path.join(docsRoot, childRel, INDEX_FILE)
            const hasIndex = fs.existsSync(dirIndex)
            const dirText = formatTitle(dirName)
            const matchingFile = fileBaseNameToFile.get(dirName)

            if (hasIndex && childItems.length === 1) {
                items.push({
                    text: dirText,
                    link: toLink(project, childRel.replace(/\\/g, '/'), true),
                })
                return
            }

            const groupLink = hasIndex
                ? toLink(project, childRel.replace(/\\/g, '/'), true)
                : matchingFile
                    ? toLink(project, path.join(dirRel, matchingFile.replace(/\.md$/, '')).replace(/\\/g, '/'), false)
                    : undefined

            items.push({
                text: dirText,
                link: groupLink,
                collapsed: depth >= 2,
                items: hasIndex ? childItems.slice(1) : childItems,
            })
        })

    return items
}

function buildFooterLinks(projects: string[], currentProject: string): DefaultTheme.SidebarItem[] {
    const otherDocs = projects
        .filter((project) => project !== currentProject)
        .map((project) => ({
            text: formatTitle(project),
            link: `/docs/${project}/`,
        }))

    const items: DefaultTheme.SidebarItem[] = [
        {text: 'Guide', link: '/guide/getting-started/introduction.html'},
        ...otherDocs,
    ]

    if (!items.length) {
        return []
    }

    return [
        {
            text: 'More',
            collapsed: true,
            items,
        },
    ]
}

export function buildDocsSidebars(docsRoot: string): Record<string, DefaultTheme.SidebarItem[]> {
    const result: Record<string, DefaultTheme.SidebarItem[]> = {}
    const projects = fs.readdirSync(docsRoot, {withFileTypes: true})
        .filter((entry) => entry.isDirectory() && !entry.name.startsWith('.'))
        .map((entry) => entry.name)
        .sort((a, b) => a.localeCompare(b))

    projects.forEach((project) => {
        const sidebarItems = readDirItems(docsRoot, project, '', 0)
        result[`/docs/${project}/`] = [
            ...sidebarItems,
            ...buildFooterLinks(projects, project),
        ]
    })

    return result
}
