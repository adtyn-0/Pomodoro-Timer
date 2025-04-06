# imports
import customtkinter as ctk
import os
from Source_Code import settings, timer_logic, watcher, theme
from PIL import ImageTk
from customtkinter import CTkImage

user_settings = settings.load_settings()
work_min = user_settings['work_minutes']

app = ctk.CTk()
app.title("Pomodoro Timer")
app.geometry("500x400")
app.resizable(True, True)

theme.apply_appearance_mode()
theme.apply_initial_theme(app)
theme.load_cat_images()

# Animated Cat Setup
cat_label = ctk.CTkLabel(app, text="")

current_animation = {
    "frames": [],
    "index": 0,
    "label": cat_label,
    "tk_imgs": []
}


def update_cat(session_type):
    frames = theme.cat_frames.get(session_type, [])
    current_animation["frames"] = frames
    current_animation["index"] = 0
    current_animation["tk_imgs"] = [ImageTk.PhotoImage(f) for f in frames]

    if frames:
        current_animation["label"].configure(
            image=current_animation["tk_imgs"][0])

    theme.apply_theme_color(app, session_type)


def animate_cat():
    if not current_animation["frames"]:
        return

    current_animation["index"] = (
        current_animation["index"] + 1) % len(current_animation["tk_imgs"])
    frame = current_animation["tk_imgs"][current_animation["index"]]
    current_animation["label"].configure(image=frame)
    app.after(120, animate_cat)


# UI Labels & Buttons
heading = ctk.CTkLabel(app, text="Pomodoro Timer",
                       font=("Orbitron", 20), text_color="white")
timer_label = ctk.CTkLabel(app, text=f"{work_min:02}:00", font=(
    "Orbitron", 48, "bold"), text_color="white")
session_label = ctk.CTkLabel(app, text='Ready', font=(
    "Orbitron", 24), text_color="white")

start_button = ctk.CTkButton(app, text="Start", font=("Orbitron", 20, "bold"),
                             fg_color="#23cb6c", hover_color="#0c9413",
                             command=lambda: timer_logic.start_work(timer_label, session_label, update_cat, app))

reset_button = ctk.CTkButton(app, text="Reset", font=("Orbitron", 20, "bold"),
                             fg_color="#8d8686", hover_color="#787171",
                             command=lambda: timer_logic.reset_timer(timer_label, session_label, app))

stop_button = ctk.CTkButton(app, text="Stop", font=("Orbitron", 20, "bold"),
                            fg_color="#cb2323", hover_color="#941313",
                            command=lambda: timer_logic.stop_timer(app))

settings_button = ctk.CTkButton(
    app, text="Settings", command=lambda: open_settings_window())


# Layout
app.grid_columnconfigure((0, 1, 2, 3), weight=1)
app.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)

settings_button.grid(row=0, column=0, sticky='nw', padx=15, pady=15)
heading.grid(row=0, column=0, columnspan=3, pady=(15, 5))
session_label.grid(row=1, column=0, columnspan=3, pady=(0, 5))
timer_label.grid(row=2, column=0, columnspan=3, pady=(10, 10))
start_button.grid(row=3, column=0, padx=10, pady=(10, 5))
stop_button.grid(row=3, column=1, padx=10, pady=(10, 5))
reset_button.grid(row=3, column=2, padx=10, pady=(10, 5))
cat_label.grid(row=5, column=0, columnspan=3, pady=(10, 20), sticky="s")


# Settings Window
def open_settings_window():
    root = os.path.dirname(os.path.dirname(__file__))
    soundfiles = [f for f in os.listdir(os.path.join(
        root, "assets/sounds")) if f.endswith(("mp3", "wav"))]

    setting_window = ctk.CTkToplevel()
    setting_window.title("Settings")
    setting_window.geometry('300x250')

    setting_window.lift()
    setting_window.focus_force()
    setting_window.grab_set()

    # Center the settings window relative to the main app
    app.update_idletasks()
    app_x = app.winfo_x()
    app_y = app.winfo_y()
    app_width = app.winfo_width()
    app_height = app.winfo_height()

    setting_window.update_idletasks()
    win_width = setting_window.winfo_width()
    win_height = setting_window.winfo_height()

    x = app_x + (app_width - win_width) // 2
    y = app_y + (app_height - win_height) // 2
    setting_window.geometry(f"+{x}+{y}")

    scroll_frame = ctk.CTkScrollableFrame(
        setting_window, width=300, height=250)
    scroll_frame.pack(padx=10, pady=10, fill='both', expand=True)

    focus_mode_var = ctk.BooleanVar(value=settings.is_focus_mode_enabled())

    ctk.CTkLabel(
        scroll_frame, text="Work Duration (in minutes): ").pack(pady=5)
    work_entry = ctk.CTkEntry(scroll_frame)
    work_entry.insert(0, str(user_settings["work_minutes"]))
    work_entry.pack(pady=5)

    ctk.CTkLabel(scroll_frame, text="Short Break (min):").pack(pady=5)
    short_break_entry = ctk.CTkEntry(scroll_frame)
    short_break_entry.insert(0, str(user_settings["short_break_minutes"]))
    short_break_entry.pack(pady=5)

    ctk.CTkLabel(scroll_frame, text="Long Break (min):").pack(pady=5)
    long_break_entry = ctk.CTkEntry(scroll_frame)
    long_break_entry.insert(0, str(user_settings["long_break_minutes"]))
    long_break_entry.pack(pady=5)

    ctk.CTkLabel(scroll_frame, text="Cycles Before Long Break:").pack(pady=5)
    cycle_entry = ctk.CTkEntry(scroll_frame)
    cycle_entry.insert(0, str(user_settings["cycles_before_long_break"]))
    cycle_entry.pack(pady=5)

    ctk.CTkLabel(scroll_frame, text="Alarm Sound:").pack(pady=5)
    sound_selector = ctk.CTkOptionMenu(scroll_frame, values=soundfiles)
    sound_selector.set(user_settings.get("alarm_sound", soundfiles[0]))
    sound_selector.pack(pady=5)

    ctk.CTkLabel(scroll_frame, text="Appearance Mode:").pack(pady=5)
    appearance_mode_var = ctk.StringVar(
        value=user_settings.get("appearance_mode", "Dark"))
    appearance_selector = ctk.CTkOptionMenu(scroll_frame,
                                            values=["Light", "Dark", "System"],
                                            variable=appearance_mode_var)
    appearance_selector.pack(pady=5)

    def save_changes():
        new_settings = {
            "work_minutes": int(work_entry.get()),
            "short_break_minutes": int(short_break_entry.get()),
            "long_break_minutes": int(long_break_entry.get()),
            "cycles_before_long_break": int(cycle_entry.get()),
            "focus_mode_enabled": focus_mode_var.get(),
            "alarm_sound": sound_selector.get(),
            "appearance_mode": appearance_mode_var.get()
        }
        ctk.set_appearance_mode(appearance_mode_var.get())
        settings.save_settings(new_settings)
        setting_window.destroy()

    ctk.CTkButton(scroll_frame, text="Save",
                  command=save_changes).pack(pady=10)

    ctk.CTkSwitch(scroll_frame, text="Enable Focus Mode",
                  variable=focus_mode_var,
                  command=lambda: watcher.toggle_focus_mode(
                      focus_mode_var.get())
                  ).pack(pady=10)


def on_closing():
    settings.toggle_mode(False)
    app.destroy()


app.protocol("WM_DELETE_WINDOW", on_closing)

update_cat("work")
animate_cat()

app.mainloop()
