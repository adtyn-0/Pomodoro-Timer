
# Pomodoro Timer

A simple, clean, and customizable Pomodoro Technique-based timer built with Python and CustomTkinter. Includes animated pixel art, configurable alarm sounds, and a built-in distraction blocker via Focus Mode.

---

## Features

### Pomodoro Cycle
- Work → Short Break → Long Break loop
- Configurable durations and cycle counts
- Automatic transition between sessions

### Modern UI
- Sleek, minimalist interface with dark/light themes
- Pixel Animation to reflect session state:
### Alarm Sound Options
- Multiple sound alerts included (classic, digital)
- Add your own `.mp3` or `.wav` files to `assets/sounds/`
- Select sound from settings

### Focus Mode
When enabled, Focus Mode monitors and closes distracting apps or tabs during work sessions.

It helps you stay on track by targeting common distractions:

```
YouTube, Twitter, Instagram, Reddit, Discord, TikTok, Facebook, Netflix, Pinterest, Telegram, WhatsApp, Steam, Epic Games, Opera GX, Chrome (distracting tabs)
```

- Auto-disabled when the app is closed (configurable)
- Can be toggled via the settings menu

---

## Configuration

User preferences are saved in `settings.json` and can be modified via the app's **Settings Panel**:

- Work session duration
- Break durations
- Cycles before long break
- Theme mode (Light, Dark, System)
- Alarm sound
- Focus Mode toggle

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/pomodoro-timer.git
cd pomodoro-timer
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the app

```bash
python run.py
```

### Run from Executable (Windows only)

Navigate to the `release/` folder and run:

```
PomodoroTimer.exe
```

## Packaging as an Executable

To build a standalone executable (Windows only):

```bash
pyinstaller --noconfirm --onefile --windowed --icon=assets/icons/pomodoro-technique.ico run.py
```

The generated `.exe` will be located in the `dist/` folder.


---

## Notes

- Works best on Windows. Linux/Mac users may need to tweak process names in Focus Mode.
- Designed to run without virtual environments; just `pip install` and go.


