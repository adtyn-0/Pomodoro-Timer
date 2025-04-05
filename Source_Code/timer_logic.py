import settings
import os
from playsound3 import playsound
import threading

count_id = None
cycle = 0


# Countdown logic with safety checks
def countdown(label, app, sec, on_complete):
    global count_id
    try:
        if not (label.winfo_exists() and app.winfo_exists()):
            print("App or label no longer exists. Cancelling countdown.")
            return
    except:
        return  # Widgets may have already been destroyed

    if sec >= 0:
        min_left = sec // 60
        sec_left = sec % 60
        try:
            label.configure(text=f"{min_left:02}:{sec_left:02}")
        except:
            return  # Avoid crash if label was destroyed

        try:
            count_id = app.after(1000, countdown, label,
                                 app, sec - 1, on_complete)
        except:
            count_id = None
            return
    else:
        count_id = None
        try:
            on_complete()
        except:
            pass


# Start Work Session
def start_work(label, session_label, app):
    global cycle
    stop_timer(app)  # Cancel previous countdown if any
    cycle += 1
    user_settings = settings.load_settings()
    work_min = user_settings["work_minutes"]
    print(f"Starting work session {cycle}")
    session_label.configure(text=f"Work Session: {cycle}")
    countdown(label, app, work_min * 60,
              lambda: [play_alarm(), start_break(label, session_label, app)])


# Start Break
def start_break(label, session_label, app):
    user_settings = settings.load_settings()
    cycle_before_long_break = user_settings["cycles_before_long_break"]
    short_break = user_settings["short_break_minutes"]
    long_break = user_settings["long_break_minutes"]

    if cycle % cycle_before_long_break == 0:
        print("Starting long break")
        session_label.configure(text="Long Break Session")
        countdown(label, app, long_break * 60,
                  lambda: [play_alarm(), start_break(label, session_label, app)])
    else:
        print("Starting short break")
        session_label.configure(text="Short Break Session")
        countdown(label, app, short_break * 60,
                  lambda: [play_alarm(), start_break(label, session_label, app)])


# Stop Timer
def stop_timer(app):
    global count_id
    if count_id:
        try:
            app.after_cancel(count_id)
            print("Timer stopped.")
        except:
            print("Failed to cancel timer (maybe app is closing).")
        count_id = None


# Reset Timer
def reset_timer(label, session_label, app):
    global cycle
    stop_timer(app)
    cycle = 0
    user_settings = settings.load_settings()
    work_min = user_settings["work_minutes"]
    try:
        label.configure(text=f"{work_min:02}:00")
        session_label.configure(text="Ready")
    except:
        pass
    print("Timer reset.")

# Add Sounds


def play_alarm():
    def play():
        # dynamically find root path
        root = os.path.dirname(os.path.dirname(__file__))

        user_settings = settings.load_settings()
        soundfile = user_settings.get("alarm_sound", "alarm_classic.mp3")
        # attach assets folder to root path
        alarm_path = os.path.join(root, "assets/sounds", soundfile)
        playsound(alarm_path)
    threading.Thread(target=play, daemon=True).start()
