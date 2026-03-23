---
# https://vitepress.dev/reference/default-theme-home-page
layout: home

hero:
  name: "PST Hibou"
  text: "Drone Detection System"
  tagline: A state of the art acoutstic detection system
  actions:
    - theme: brand
      text: Getting started
      link: /guide/getting-started/introduction

features:
  - title: Detection
    icon: <span class="i-carbon:satellite-radar"></span>
    details: Use ML/AI models to detect drones in the area.
  - title: Confirmation
    icon: <span class="i-carbon:video-chat"></span>
    details: Confirmation of the drone using ML/AI and see the live stream of it.
  - title: Localization
    icon: <span class="i-carbon:location-info">
    details: Algorithms to localize the drone in the area using Detection data & Confirmation data.

  - title: Server
    icon: <span class="i-carbon:bare-metal-server"></span>
    details: Look at the docs for the Detection Server part.
    link: /docs/server/
    linkText: Take a look
  - title: Client
    icon: <span class="i-carbon:application-web"></span>
    details: Docs concerning the Web Server of part.
    link: /docs/client/
    linkText: Take a look
  - title: Guide
    icon: <span class="i-carbon:book"></span>
    details: See technical and practical information about the project.
    link: /guide/getting-started/introduction.html
    linkText: Get started
---
