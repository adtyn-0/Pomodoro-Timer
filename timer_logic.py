import tkinter as tk


class Timer:
    def __init__(self, root):
        self.root = root
        self.root.title("Digital Timer")
        self.running = False
        self.time = 0
        self.label = tk.Label(root, text=self.format_time(
            self.time), font=("Helvetica", 48))
        self.label.pack()
        self.start_button = tk.Button(root, text="Start", command=self.start)
        self.start_button.pack(side="left")
        self.stop_button = tk.Button(root, text="Stop", command=self.stop)
        self.stop_button.pack(side="left")
        self.reset_button = tk.Button(root, text="Reset", command=self.reset)
        self.reset_button.pack(side="left")

    def format_time(self, t):
        mins, secs = divmod(t, 60)
        hours, mins = divmod(mins, 60)
        return f"{hours:02}:{mins:02}:{secs:02}"

    def update_timer(self):
        if self.running:
            self.time += 1
            self.label.config(text=self.format_time(self.time))
            self.root.after(1000, self.update_timer)

    def start(self):
        if not self.running:
            self.running = True
            self.update_timer()

    def stop(self):
        self.running = False

    def reset(self):
        self.running = False
        self.time = 0
        self.label.config(text=self.format_time(self.time))


root = tk.Tk()
timer = Timer(root)
root.mainloop()
