import os
import json

settings_file = "settings.json"

default_settings = {
    "work_minutes": 25,
    "short_break_minutes": 5,
    "long_break_minutes": 15,
    "cycles_before_long_break": 4,
    "focus_mode_enabled": False
}


# Load Pre-existing user settings
def load_settings():
    if os.path.exists(settings_file):
        with open(settings_file, 'r') as file:
            return json.load(file)
    else:
        return default_settings


# Save new settings
def save_settings(settings):
    with open(settings_file, 'w') as file:
        json.dump(settings, file, indent=4)


# checks for Focus Mode
def is_focus_mode_enabled():
    settings = load_settings()
    return settings.get('focus_mode_enabled', False)


def toggle_mode(enabled: bool):
    settings = load_settings()
    settings["focus_mode_enabled"] = enabled
    save_settings(settings)
