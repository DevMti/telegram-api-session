# Telegram API & Session Creator

A Python tool for generating or retrieving Telegram API credentials (API ID and API Hash) and creating Pyrogram session strings for automation workflows.

> ⚠️ This tool interacts with https://my.telegram.org and requires a valid Telegram account.

---

## Features

- 🔑 Retrieve or generate Telegram **API ID & API Hash**
- 🤖 Automates login flow via `my.telegram.org`
- 💾 Generates **Pyrogram session strings**
- 📁 Saves session data locally as a `.txt` file
- ⚡ Simple interactive CLI

---

## Requirements

- Python **3.10+** (recommended: 3.11 or 3.12)
- Internet connection
- A Telegram account

---

## Setup (Recommended: uv + virtual environment)

This project uses **uv** for fast dependency management and virtual environments.

### 1. Install uv

If you don't already have `uv` installed:

```bash
curl -Ls https://astral.sh/uv/install.sh | sh
```

or:
```bash
pip install uv
```

### 2. Create a virtual environment

Inside the project folder:

```bash
uv venv .venv
```

This creates an isolated Python environment inside `.venv`.

### 3. Activate the environment

Linux / macOS:

```bash
source .venv/bin/activate
```

Windows (PowerShell):

```bash
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

If you have a requirements.txt:

```bash
uv pip install -r requirements.txt
```

If not, install manually:

```bash
uv pip install pyrogram tgcrypto requests beautifulsoup4
```

### Running the project

After activating the virtual environment:

```bash
python main.py
```

### Project Structure
telegram-api-session/
├── main.py
├── requirements.txt
├── pyproject.toml (optional)
├── .venv/
└── session_output.txt

### Disclaimer

This project is for educational purposes only.
Users are responsible for complying with Telegram’s Terms of Service.