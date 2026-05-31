---
name: android-cli
description: Orchestrates Android development tasks including project creation, deployment, SDK management, and environment diagnostics using the `android` command-line tool.
---
# Android CLI Specialist

This skill provides instructions for using the `android` CLI tool. The tool includes various commands for creating projects, running applications, interacting with devices, and managing the CLI environment.

## Installation

If the android tool is not in the path install it. To install run the following command:
- Linux: `curl -fsSL https://dl.google.com/android/cli/latest/linux_x86_64/install.sh | bash`
- Mac: `curl -fsSL https://dl.google.com/android/cli/latest/darwin_arm64/install.sh | bash`
- Windows: `curl.exe -fsSL https://dl.google.com/android/cli/latest/windows_x86_64/install.cmd -o "%TEMP%\i.cmd" && "%TEMP%\i.cmd"`

## SDK management
To manage the installation of Android SDKs and tools, use the `sdk` command. For example:
- `android sdk install <package>[@<version>]...` – Install specific packages (multiple packages separated by spaces). `<version>` defaults to latest. Example: `android sdk install platforms/android-30@2 platforms/android-34`.
- `android sdk update [<pkg-name>]` – Update a specific package or all packages.
- `android sdk remove <pkg-name>` – Remove a package.
- `android sdk list --all` – List installed and available SDK packages.

## Project creation
Create projects from templates using the `create` command.

Example: `android create empty-activity --name="My App" --output=./my-app`

## Interacting with devices
For more information on interacting with running devices, see the `references/interact.md` document.

## Running journey tests
For more information on running journeys, see the `references/journeys.md` document.

## Doc searching
The `docs` command searches authoritative Android developer documentation.
- `android docs search <keywords>` – Search documentation.
- `android docs fetch <doc-id>` – Retrieve a specific document.

Typical use‑cases:
- Finding migration guides.
- Getting code examples.
- Looking up API best practices.

## Running APKs
Use the `run` command to deploy and run Android applications.

## Managing emulators
Manage Android Virtual Devices (AVDs) via `android emulator` sub‑commands.

## Capturing screenshots
Capture the screen of a connected device with `android screenshot` and output to a file.

## Managing skills
Use `android skills` to list, add, remove, or find Antigravity agent skills related to Android.

## Inspecting UI Layouts
`android layout` returns the UI layout tree of an app in JSON format, useful for fast debugging.

## Updating the CLI
`android update` updates the Android CLI to the latest version.

# `android help` output
```
Usage: android [-hV] [--sdk=PARAM] [COMMAND]
  -h, --help        Show this help message and exit.
      --sdk=PARAM   Path to the Android SDK
  -V, --version     Print version information and exit.
Commands:
  create    Create a new Android project
  describe  Analyze an Android project and generate metadata
  docs      Documentation search commands
  emulator  Emulator management commands
  help      Show help for commands
  info      Print environment information
  init      Initialize the Android CLI environment
  layout    Dump UI layout tree (JSON)
  run       Deploy and run an Android app
  screen    Device screen commands (capture, resolve)
  sdk       SDK package management
  skills    Manage Antigravity Android skills
  update    Update the Android CLI
```

## Sub‑command details (excerpt)

### create
```
android create [-h] [--verbose] [--list] [--minSdk=api] --name=applicationName [-o=dest-path] [template-name]
```
- `--minSdk=api` – Minimum SDK version (default from template).
- `--name` – Application name.
- `-o` – Destination directory (default current directory).
- `--list` – List available project templates.

### describe
```
android describe [-hV] [--project_dir=PATH]
```
Generates JSON metadata describing build targets, APK locations, etc.

### docs
```
android docs [-h] COMMAND
Commands:
  search <keywords> – Search docs.
  fetch <doc-id>    – Retrieve a specific doc.
```

### emulator
```
android emulator [COMMAND]
Commands:
  create  – Create a new AVD.
  start   – Start an AVD (waits until ready).
  stop    – Stop an AVD.
  list    – List available AVDs.
  remove  – Delete an AVD.
```

### layout
```
android layout [-dhp] [--device=SERIAL] [-o=OUTPUT]
```
- `-d` – Show diff since last dump.
- `-p` – Pretty‑print JSON.
- `--device` – Target device serial.
- `-o` – Output file.

### run
```
android run [--debug] [--activity=NAME] [--device=SERIAL] [--type=COMPONENT] --apks=APK1[,APK2...]
```
Deploys one or more APKs to the specified device.

### screen
```
android screen capture [--output=FILE]
android screen resolve <selector>
```
Capture a screenshot or resolve UI elements visually.

### sdk
```
android sdk install <pkg[@ver]> ...
android sdk update [<pkg>]
android sdk remove <pkg>
android sdk list --all
```

### skills
```
android skills list
android skills add <skill-id>
android skills remove <skill-id>
android skills find <keyword>
```

### update
```
android update [--url=URL]
```
Updates the CLI.

---
**End of Android CLI skill definition**
