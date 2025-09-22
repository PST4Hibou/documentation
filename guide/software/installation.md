# Installation

Install uv to manage env, dependencies, python...

 ```
 curl -LsSf https://astral.sh/uv/install.sh | sh
 ```

First install linux dependencies 

```
sudo dnf install cairo-devel pkg-config python3-devel gcc cairo-gobject-devel gobject-introspection-deve
```

::: warning
Don't forget to clone the .env.exemple as .env
:::

Run the program, it will install the python dependencies
```
uv run main.py
```