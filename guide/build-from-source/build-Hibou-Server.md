# Build Hibou Server

Hibou Server is a development-focused software project designed to manage and process audio and video input for AI-driven applications.
It provides modules for audio processing, computer vision, device management, and PTZ camera control.
This documentation describes how to build and run the latest development version of Hibou Server.

The development version of Hibou Server is primarily intended for software developers
and technical users who want to contribute to the project or experiment with advanced features.
If you simply want to run the software without building it from source, you can download the latest release [here](https://).
For any help, please visit our [forum](https://discord.gg/mhaZFqKA).

## System Requirements

For the best performance, 
stability, and functionality we have documented some recommendations for running a Nextcloud server.

| Platform                  | Options                                                                                                      |
|---------------------------|--------------------------------------------------------------------------------------------------------------|
| Operating System (64 bit) | - Ubuntu 25.10<br/>- **Fedora** 43 (recommended)<br/>- **Ubuntu 24.04 LTS** (recommended)<br/>- Alpine Linux |
| Python                    | - **3.13** (recommended)<br/> - 3.12<br/>- 3.11<br/>                                                         |
| RAM                       | - **16 Go or above** (recommended)<br/>- 8 Go                                                                |

::: info
It should be possible to run the software on other operating systems like Windows, but this is not officially supported.
:::

## Project Architecture

The folder structure below shows the main modules and files of the Hibou Server project.

```shell
.
├── assets                    # Local AI models
├── in                        # Mics input folder for emulation. (Debug only)
├── logs                      # App logs folder
├── recs                      # Audio recordings folder (Debug only)
├── src                       # Source folder
│   ├── audio                 # Audio module
│   ├── computer_vision       # Drone detection by AI using video stream
│   ├── devices               # ADC devices for microphones
│   ├── helpers               # Helpfully functions
│   ├── network
│   └── ptz                   # PTZ camera source code
├── devices.json              # device configuration file
├── logging.conf              # Python logging config file
├── main.py                   # main python program
├── pyproject.toml            # uv configuration file
└── README.md
```


## Dependencies installation

To build the software, you will need to install the following dependencies:

### System dependencies

::: code-group

```shell [ubuntu]
$ sudo apt install -y git curl gcc tshark pkg-config portaudio19-dev g++ python3-pip python3-cairo-dev libjpeg8-dev libpango1.0-dev libgif-dev build-essential python3-gi python3-gi-cairo gir1.2-gtk-4.0 libgirepository-2.0-dev libcairo2-dev
```

```shell [fedora]
$ sudo dnf install -y git curl gcc tshark pkgconf portaudio-devel python3.13-devel  gobject-introspection-devel cairo-gobject-devel gtk4
```
:::

### Install uv

UV is a fast Python package and project manager written in Rust.
It serves as a modern alternative to traditional Python package managers like pip and poetry, offering significantly faster installation times and better dependency resolution.
UV can manage Python versions, create virtual environments, and handle project dependencies with a single unified tool.

::: code-group

```shell [curl]
$ curl -LsSf https://astral.sh/uv/install.sh | sh
```

```shell [pip]
$ pip install uv
```

```shell [pipx]
$ pipx install uv
```
:::


::: info
If using curl, make sure the bin folder is in your PATH environment variable.
If not run: 
```shell 
$ export PATH="/home/$USER/.local/bin:$PATH"`.
```
For a permanent solution, add the line to your `.bashrc` file.
:::

## Run tshark as non-root

::: info
If you don't plan to use the auto discovery feature, you can safely skip the section.
:::

Tshark is a tool that uses the wireshark engine to capture packets.
Since we use a proprietary device like Dante and auto-discovery over network,
there is no open protocol to get device configuration like rtp-payload or clock rate.
One "easy" solution is to capture packets and retrieve information from them.

By default, capturing packets requires root privileges because it involves accessing network interfaces directly.
To avoid running your application as root, you can allow non-privileged users to capture packets by assigning them to the wireshark group:

```shell
$ usermod -aG wireshark $USER
```

After updating group membership, log out or reboot to apply the change.

You can verify permissions using:

```shell
$ tshark -D
```
If the interfaces are listed without permission errors, the setup is correct.


## Getting the code

To get the code, clone the repository:

```shell
$ git clone git@github.com:PST4Hibou/Hibou-Server.git
```

## Running

In the project directory, run the following command:
```shell
$ cd Hibou-Server/
$ uv run main.py
```

`uv run` will automatically installed the dependencies and run the program.

If you don't want to run the program, run:

```shell
$ uv sync
```


## Debug

To know more about debugging, please refer to the [debug page](/guide/debug/hibou-server.html)
