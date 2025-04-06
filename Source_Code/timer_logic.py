from Source_Code import settings, timer_logic, watcher, theme
import os
import sys
from playsound3 import playsound
import threading

count_id = None
cycle = 0

# for pyinstaller


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(__file__), '..', relative_path)


def countdown(label, app, sec, on_complete):
    global count_id
    try:
        if not (label.winfo_exists() and app.winfo_exists()):
            print("App or label no longer exists. Cancelling countdown.")
            return
    except:
        return

    if sec >= 0:
        min_left = sec // 60
        sec_left = sec % 60
        try:
            label.configure(text=f"{min_left:02}:{sec_left:02}")
        except:
            return
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


def start_work(label, session_label, update_cat, app):
    global cycle
    stop_timer(app)
    cycle += 1
    user_settings = settings.load_settings()
    work_min = user_settings["work_minutes"]
    update_cat("work")
    print(f"Starting work session {cycle}")
    session_label.configure(text=f"Work Session: {cycle}")
    countdown(label, app, work_min * 60,
              lambda: next_phase("work", label, session_label, update_cat, app))


def start_break(label, session_label, update_cat, app, long_break=False):
    user_settings = settings.load_settings()

    if long_break:
        duration = user_settings["long_break_minutes"]
        label_type = "Long Break"
        cat_type = "long_break"
    else:
        duration = user_settings["short_break_minutes"]
        label_type = "Short Break"
        cat_type = "short_break"

    print(f"Starting {label_type.lower()}")
    session_label.configure(text=f"{label_type} Session")
    update_cat(cat_type)
    countdown(label, app, duration * 60,
              lambda: next_phase("break", label, session_label, update_cat, app))


def next_phase(last_session, label, session_label, update_cat, app):
    play_alarm()
    user_settings = settings.load_settings()
    global cycle

    if last_session == "work":
        if cycle % user_settings["cycles_before_long_break"] == 0:
            start_break(label, session_label, update_cat, app, long_break=True)
        else:
            start_break(label, session_label, update_cat,
                        app, long_break=False)
    else:
        start_work(label, session_label, update_cat, app)


def stop_timer(app):
    global count_id
    if count_id:
        try:
            app.after_cancel(count_id)
            print("Timer stopped.")
        except:
            print("Failed to cancel timer.")
        count_id = None


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


def play_alarm():
    def play():
        user_settings = settings.load_settings()
        soundfile = user_settings.get("alarm_sound", "alarm_classic.mp3")
        alarm_path = resource_path(os.path.join("assets/sounds", soundfile))
        playsound(alarm_path)

    threading.Thread(target=play, daemon=True).start()
