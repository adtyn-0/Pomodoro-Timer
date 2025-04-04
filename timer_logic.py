import time
import settings

count_id = None
cycle = 0


# Countdown logic
def countdown(label, app, sec, on_complete):
    global count_id
    if sec >= 0:
        min_left = sec // 60
        sec_left = sec % 60
        label.configure(text=f"{min_left:02}:{sec_left:02}")
        count_id = app.after(1000, countdown, label, app, sec - 1, on_complete)
    else:
        count_id = None
        on_complete()


# Start Work Session
def start_work(label, app):
    global cycle
    stop_timer(app)  # Cancel previous countdown if any
    cycle += 1
    user_settings = settings.load_settings()
    work_min = user_settings["work_minutes"]
    print(f"Starting work session {cycle}")
    countdown(label, app, work_min * 60, lambda: start_break(label, app))


# Start Break
def start_break(label, app):
    user_settings = settings.load_settings()
    cycle_before_long_break = user_settings["cycles_before_long_break"]
    short_break = user_settings["short_break_minutes"]
    long_break = user_settings["long_break_minutes"]

    if cycle % cycle_before_long_break == 0:
        print("Starting long break")
        countdown(label, app, long_break * 60, lambda: start_work(label, app))
    else:
        print("Starting short break")
        countdown(label, app, short_break * 60, lambda: start_work(label, app))


# Stop Timer
def stop_timer(app):
    global count_id
    if count_id:
        app.after_cancel(count_id)
        count_id = None
        print("Timer stopped.")


# Reset Timer
def reset_timer(label, app):
    global cycle
    stop_timer(app)
    cycle = 0
    user_settings = settings.load_settings()
    work_min = user_settings["work_minutes"]
    label.configure(text=f"{work_min:02}:00")
    print("Timer reset.")
