# Installation

The Hibou Web Interface is a web application that allows users to have a graphical interface to see the environment, the drones, the parabolics and to have a better understanding of the data.

It is built with Vue.js, Nuxt.js and FastAPI. It communicates with the backend via the zeromq IPC used in the Hibou-Server project. 


Located in the repository https://github.com/PST4Hibou/Hibou-Interface

## How to run, frontend

To install the frontend, you need to have Node.js and npm installed on your machine. Then, you can run the following commands in the frontend directory:

```bash
pnpm install
```

This will install all the dependencies of the project. After that, you can run the following command to start the development server:

```bash
pnpm run dev
```

You should also populate the .env with your mapbox access token :

```bash
NUXT_PUBLIC_MAPBOX_ACCESS_TOKEN={YOURTOKEN}
```

This will start the development server and you can access the web interface at `http://localhost:3000`.

## How to run, backend

To install the backend, like the Hibou-Server, you should use `uv`
```bash
uv run fastapi --reload
```

Before logging in, you need to create an account. First enable registration by temporarily commenting out the early raise in backend/api/auth.py:31-34.
Then use the following curl command to create an account:


```bash
curl -X POST http://localhost:8000/auth/register -H "Content-Type: application/json" -d '{"identifier": "admin", "password": "SuperSecurePassword"}'
```