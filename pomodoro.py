# imports
import customtkinter as ctk
import settings
import watcher
import timer_logic

user_settings = settings.load_settings()
work_min = user_settings['work_minutes']
# Main Window
app = ctk.CTk()
app.title("Pomodoro Timer")
app.geometry("400x300")
app.resizable(True, True)
app.configure(fg_color="#406182")


# Timer Labels
timer_label = ctk.CTkLabel(app, text=f"{work_min: 02}:00", font=(
    "Orbitron", 40, "bold"), text_color="white")


start_button = ctk.CTkButton(
    app, text="Start", font=(
        "Orbitron", 20, "bold"), fg_color="#23cb6c", hover_color="#0c9413", command=lambda: timer_logic.start_work(timer_label, app))


reset_button = ctk.CTkButton(app, text="Reset", font=(
    "Orbitron", 20, "bold"), fg_color="#8d8686", hover_color="#787171", command=lambda: timer_logic.reset_timer(timer_label, app)
)

stop_button = ctk.CTkButton(app, text="Stop", font=("Orbitron", 20, "bold"), fg_color="#cb2323",  hover_color="#941313", command=lambda: timer_logic.stop_timer(app)
                            )


# SETTINGS
def settings_window():
    setting_window = ctk.CTkToplevel()
    setting_window.title("Settings")
    setting_window.geometry('300x250')

    # Scroll Fix
    scroll_frame = ctk.CTkScrollableFrame(
        setting_window, width=300, height=250)
    scroll_frame.pack(padx=10, pady=10, fill='both', expand=True)

    # Toggle for Focus Mode
    focus_mode_var = ctk.BooleanVar(value=settings.is_focus_mode_enabled())

    # Fields
    ctk.CTkLabel(scroll_frame,
                 text="Work Duration (in minutes): ").pack(pady=5)
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

    # Saving the changes
    def save_changes():
        new_settings = {
            "work_minutes": int(work_entry.get()),
            "short_break_minutes": int(short_break_entry.get()),
            "long_break_minutes": int(long_break_entry.get()),
            "cycles_before_long_break": int(cycle_entry.get()),

        }
        new_settings["focus_mode_enabled"] = focus_mode_var.get()
        settings.save_settings(new_settings)
        setting_window.destroy()

    save_button = ctk.CTkButton(
        scroll_frame, text="Save", command=save_changes)
    save_button.pack(pady=10)

    # Toggle Button
    def toggle_focus():
        enabled = focus_mode_var.get()
        watcher.toggle_focus_mode(enabled)
        settings.toggle_mode(enabled)

    focus_mode_switch = ctk.CTkSwitch(
        scroll_frame,
        text="Enable Full Focus Mode",
        variable=focus_mode_var,
        command=toggle_focus
    )
    focus_mode_switch.pack(pady=10)


settings_button = ctk.CTkButton(
    app, text="Settings", command=settings_window
)


def on_closing():
    settings.toggle_mode(False)
    app.destroy()


# Layout
timer_label.grid(row=1, column=1, padx=0, pady=0)
start_button.grid(row=3, column=0, padx=0, pady=0)
stop_button.grid(row=2, column=0, padx=0, pady=0)
reset_button.grid(row=5, column=0, padx=0, pady=0)
settings_button.grid(row=0, column=0, padx=0, pady=0)

app.protocol("WM_DELETE_WINDOW", on_closing)  # Runs on window close


app.mainloop()
