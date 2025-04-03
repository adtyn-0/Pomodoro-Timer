import time

count_id = None
work_min = 25
cycle = 0
cycle_before_long_break = 4
short_break = 5
long_break = 15


# Countdown
def countdown(label, app, sec, on_complete):
    global count_id
    if sec >= 0:
        min_left = sec//60
        sec_left = sec % 60
        t_format = f'{min_left:02}:{sec_left:02}'

        label.configure(text=t_format)
        count_id = app.after(1000, countdown, label, app, sec-1, on_complete)
    else:
        on_complete()


# Start
def start_work(label, app):
    global cycle
    cycle += 1
    print(f"Starting work session {cycle}")
    countdown(label, app, work_min*60, lambda: start_break(label, app))


def start_break(label, app):
    global cycle
    if cycle % cycle_before_long_break == 0:
        print("Long break")
        countdown(label, app, long_break*60, lambda: start_work(label, app))
    else:
        print("ShortBreak")
        countdown(label, app, short_break*60, lambda: start_work(label, app))


# Stop
def stop_timer(app):
    global count_id
    if count_id:
        app.after_cancel(count_id)
        count_id = None


# Reset
def reset_timer(label, app):
    global cycle
    stop_timer(app)
    cycle = 0
    label.configure(text=f'{work_min:02}')
