# SUPREME AI — Voice + Text + Windows System Control

## Requirements
- Windows 10/11
- Python 3.10+
- Ollama installed and running
- Chrome or Edge for browser microphone recognition

## Setup
Open PowerShell in this project folder:

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Install/download an Ollama model (example):

```powershell
ollama pull llama3.2
```

Make sure Ollama is running, then start this app:

```powershell
python app.py
```

Open `http://127.0.0.1:5000` in Chrome or Edge.

## Supported local actions
- `open notepad`
- `open calculator`
- `open file explorer`
- `open chrome`
- `open edge`
- `open vscode`
- `open desktop`
- `open documents`
- `open downloads`
- `system info`

Edit `APP_COMMANDS` in `system_control.py` to add trusted applications.

## Voice
Press **Start voice**, allow microphone access, and speak. Browser speech recognition transcribes your command.
Replies are spoken using the browser's speech synthesis. Text input remains available.

## Security
- Flask binds to 127.0.0.1 only. Do not change this to 0.0.0.0 or expose it publicly.
- Do not add an unrestricted `os.system`, `shell=True`, or arbitrary terminal execution endpoint.
- Keep app launching allowlisted.
- Add confirmation flows before implementing file deletion, shutdown, restart, or other destructive actions.
- Browser speech recognition may use your browser's speech service; it is not guaranteed to be fully offline.

## Troubleshooting
- `ollama` not found: install Ollama and reopen PowerShell.
- Model missing: run `ollama pull llama3.2`.
- Ollama connection error: run `ollama list` and check `http://127.0.0.1:11434`.
- `code` not found: enable the VS Code `code` command in PATH or add the full executable path to `APP_COMMANDS`.
- Microphone unavailable: use Chrome/Edge and allow microphone permission.
