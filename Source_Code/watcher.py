import time
from Source_Code import settings, timer_logic, watcher, theme
import customtkinter as ctk
import threading
import pyautogui

Distraction = ["youtube", "twitter",
               "instagram", "reddit", "discord", "tiktok"]
focus_thread = None


# Show Warning Overlay
def show_warning():
    warning = ctk.CTk()
    warning.title("Stay Focused !!")
    warning.geometry('500x400')
    warning.resizable(False, False)

    label = ctk.CTkLabel(warning, text="You Opened a distracting site!!!\nStay Focused!!", font=(
        "Orbitron", 20, "bold"))
    label.pack(pady=20)

    dismiss_button = ctk.CTkButton(
        warning, text="Okay , I will focus", command=warning.destroy)

    dismiss_button.pack(pady=10)

    warning.mainloop()


# Check for Distraction
def check_distractions():
    while settings.is_focus_mode_enabled():
        active_window = pyautogui.getActiveWindow()

        if active_window:
            title = active_window.title.lower()
            if any(site in title for site in Distraction):
                show_warning()
                time.sleep(5)
        else:
            print("No active window detected.")

        time.sleep(2)


def toggle_focus_mode(enabled: bool):
    global focus_thread

    settings.toggle_mode(enabled)
    if enabled:
        if not focus_thread or not focus_thread.is_alive():
            focus_thread = threading.Thread(
                target=check_distractions, daemon=True)
            focus_thread.start()
        return True
    else:
        return True
