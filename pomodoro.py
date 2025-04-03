# imports
import customtkinter as ctk
import settings
import blocker
import timer_logic

# Main Window
app = ctk.CTk()
app.title("Pomodoro Timer")
app.geometry("400x300")
app.resizable(True, True)
app.configure(fg_color="#406182")

# Timer Labels
timer_label = ctk.CTkLabel(app, text="25:00", font=(
    "Orbitron", 40, "bold"), text_color="white")


start_button = ctk.CTkButton(
    app, text="Start", font=(
        "Orbitron", 20, "bold"), fg_color="#23cb6c", hover_color="#0c9413", command=lambda: timer_logic.start_work(timer_label, app))


reset_button = ctk.CTkButton(app, text="Reset", font=(
    "Orbitron", 20, "bold"), fg_color="#8d8686", hover_color="#787171", command=lambda: timer_logic.reset_timer(timer_label, app)
)

stop_button = ctk.CTkButton(app, text="Stop", font=("Orbitron", 20, "bold"), fg_color="#cb2323",  hover_color="#941313", command=lambda: timer_logic.stop_timer(app)
                            )


timer_label.grid(row=1, column=1, padx=0, pady=0)
start_button.grid(row=3, column=0, padx=0, pady=0)
stop_button.grid(row=2, column=0, padx=0, pady=0)
reset_button.grid(row=0, column=0, padx=0, pady=0)

app.mainloop()
