import tkinter as tk
from tkinter import messagebox


class CountdownTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Countdown Clock and Timer")
        self.root.geometry("450x400")
        self.root.resizable(False, False)
        self.root.configure(bg="#202A44")

        self.remaining = 0
        self.running = False
        self.after_id = None

        # Project title
        tk.Label(
            root,
            text="Countdown Clock and Timer",
            font=("Arial", 20, "bold"),
            bg="#202A44",
            fg="white"
        ).pack(pady=20)

        # Time input section
        input_frame = tk.Frame(root, bg="#202A44")
        input_frame.pack(pady=10)

        self.hours = tk.StringVar(value="0")
        self.minutes = tk.StringVar(value="1")
        self.seconds = tk.StringVar(value="0")

        for i, (label, variable) in enumerate([
            ("Hours", self.hours),
            ("Minutes", self.minutes),
            ("Seconds", self.seconds)
        ]):
            tk.Label(
                input_frame,
                text=label,
                font=("Arial", 11),
                bg="#202A44",
                fg="white"
            ).grid(row=0, column=i, padx=10)

            tk.Entry(
                input_frame,
                textvariable=variable,
                width=6,
                justify="center",
                font=("Arial", 14)
            ).grid(row=1, column=i, padx=10, pady=5)

        # Countdown display
        self.display = tk.Label(
            root,
            text="00:01:00",
            font=("Arial", 36, "bold"),
            bg="#202A44",
            fg="#00E5FF"
        )
        self.display.pack(pady=20)

        # Buttons
        button_frame = tk.Frame(root, bg="#202A44")
        button_frame.pack(pady=10)

        tk.Button(
            button_frame, text="Start",
            command=self.start,
            width=9, bg="#28A745", fg="white"
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            button_frame, text="Pause",
            command=self.pause,
            width=9, bg="#FFC107", fg="black"
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            button_frame, text="Reset",
            command=self.reset,
            width=9, bg="#DC3545", fg="white"
        ).grid(row=0, column=2, padx=5)

        tk.Label(
            root,
            text="Set your time and press Start",
            font=("Arial", 10),
            bg="#202A44",
            fg="white"
        ).pack(pady=10)

    def start(self):
        if self.running:
            return

        if self.remaining == 0:
            try:
                h = int(self.hours.get())
                m = int(self.minutes.get())
                s = int(self.seconds.get())

                if h < 0 or m < 0 or s < 0:
                    raise ValueError

                self.remaining = h * 3600 + m * 60 + s

            except ValueError:
                messagebox.showerror(
                    "Invalid Input",
                    "Please enter valid non-negative integers."
                )
                return

            if self.remaining <= 0:
                messagebox.showwarning(
                    "Invalid Time",
                    "Please enter a time greater than zero."
                )
                return

        self.running = True
        self.tick()

    def tick(self):
        if not self.running:
            return

        hours = self.remaining // 3600
        minutes = (self.remaining % 3600) // 60
        seconds = self.remaining % 60

        self.display.config(
            text=f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        )

        if self.remaining <= 0:
            self.running = False
            self.after_id = None
            self.root.bell()
            messagebox.showinfo("Finished", "Time is up!")
            return

        self.remaining -= 1
        self.after_id = self.root.after(1000, self.tick)

    def pause(self):
        if self.running:
            self.running = False

            if self.after_id is not None:
                self.root.after_cancel(self.after_id)
                self.after_id = None

    def reset(self):
        self.running = False

        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
            self.after_id = None

        self.remaining = 0
        self.hours.set("0")
        self.minutes.set("1")
        self.seconds.set("0")
        self.display.config(text="00:01:00")


# Main program
if __name__ == "__main__":
    root = tk.Tk()
    app = CountdownTimer(root)
    root.mainloop()