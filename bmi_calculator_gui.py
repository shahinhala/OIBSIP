import tkinter as tk
from tkinter import messagebox

# BMI Calculator GUI
# Python Programming Internship Project

BG = "#F3F5FB"
CARD = "#FFFFFF"
TEXT = "#20243A"
MUTED = "#737A91"
ACCENT = "#6558D3"
ACCENT_DARK = "#5145B8"
BORDER = "#E2E6F0"


class BMICalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BMI Calculator")
        self.root.geometry("560x690")
        self.root.minsize(500, 650)
        self.root.configure(bg=BG)

        self.weight_var = tk.StringVar()
        self.height_var = tk.StringVar()

        self.build_ui()

    def build_ui(self):
        header = tk.Frame(self.root, bg=BG)
        header.pack(fill="x", padx=30, pady=(25, 16))

        tk.Label(
            header, text="WELLNESS TOOLS", font=("Segoe UI", 9, "bold"),
            bg=BG, fg=ACCENT
        ).pack(anchor="w")

        tk.Label(
            header, text="BMI Calculator", font=("Segoe UI", 25, "bold"),
            bg=BG, fg=TEXT
        ).pack(anchor="w", pady=(5, 2))

        tk.Label(
            header, text="Calculate your Body Mass Index in seconds.",
            font=("Segoe UI", 10), bg=BG, fg=MUTED
        ).pack(anchor="w")

        card = tk.Frame(self.root, bg=CARD, highlightbackground=BORDER,
                        highlightthickness=1)
        card.pack(fill="both", expand=True, padx=30, pady=(0, 20))

        tk.Label(card, text="Enter your measurements",
                 font=("Segoe UI", 14, "bold"), bg=CARD, fg=TEXT
                 ).pack(anchor="w", padx=24, pady=(24, 18))

        self.add_input(card, "Weight", "Kilograms (kg)", self.weight_var, "e.g. 60")
        self.add_input(card, "Height", "Centimeters (cm)", self.height_var, "e.g. 165")

        self.calculate_button = tk.Button(
            card, text="Calculate BMI", command=self.calculate_bmi,
            font=("Segoe UI", 11, "bold"), bg=ACCENT, fg="white",
            activebackground=ACCENT_DARK, activeforeground="white",
            relief="flat", cursor="hand2", bd=0, pady=12
        )
        self.calculate_button.pack(fill="x", padx=24, pady=(20, 12))

        self.result_card = tk.Frame(card, bg="#F7F6FF",
                                    highlightbackground="#E5E1FF",
                                    highlightthickness=1)
        self.result_card.pack(fill="x", padx=24, pady=(4, 12))

        tk.Label(self.result_card, text="YOUR BMI RESULT",
                 font=("Segoe UI", 8, "bold"), bg="#F7F6FF", fg=MUTED
                 ).pack(pady=(14, 2))

        self.bmi_value = tk.Label(self.result_card, text="—",
                                  font=("Segoe UI", 30, "bold"),
                                  bg="#F7F6FF", fg=ACCENT)
        self.bmi_value.pack()

        self.category_label = tk.Label(self.result_card, text="Enter your details to begin",
                                       font=("Segoe UI", 11, "bold"),
                                       bg="#F7F6FF", fg=TEXT)
        self.category_label.pack(pady=(0, 5))

        self.advice_label = tk.Label(
            self.result_card,
            text="BMI is a screening measure, not a diagnosis.",
            font=("Segoe UI", 9), bg="#F7F6FF", fg=MUTED,
            wraplength=420, justify="center"
        )
        self.advice_label.pack(padx=12, pady=(0, 14))

        tk.Label(
            card,
            text="Adult reference ranges: <18.5 Underweight  •  18.5–24.9 Normal\n"
                 "25–29.9 Overweight  •  30+ Obesity",
            font=("Segoe UI", 8), bg=CARD, fg=MUTED,
            justify="center", wraplength=440
        ).pack(padx=18, pady=(4, 18))

        footer = tk.Frame(self.root, bg=BG)
        footer.pack(fill="x", padx=30, pady=(0, 16))
        tk.Label(footer, text="Python • Tkinter GUI",
                 font=("Segoe UI", 8), bg=BG, fg=MUTED).pack(side="left")
        tk.Button(footer, text="Reset", command=self.reset,
                  font=("Segoe UI", 9), bg=BG, fg=ACCENT,
                  activebackground=BG, relief="flat", cursor="hand2"
                  ).pack(side="right")

    def add_input(self, parent, label, subtitle, variable, placeholder):
        wrapper = tk.Frame(parent, bg=CARD)
        wrapper.pack(fill="x", padx=24, pady=(0, 12))

        top = tk.Frame(wrapper, bg=CARD)
        top.pack(fill="x")
        tk.Label(top, text=label, font=("Segoe UI", 10, "bold"),
                 bg=CARD, fg=TEXT).pack(side="left")
        tk.Label(top, text=subtitle, font=("Segoe UI", 9),
                 bg=CARD, fg=MUTED).pack(side="right")

        entry = tk.Entry(
            wrapper, textvariable=variable, font=("Segoe UI", 11),
            bg="#FAFBFE", fg=TEXT, insertbackground=TEXT,
            relief="flat", highlightthickness=1,
            highlightbackground=BORDER, highlightcolor=ACCENT
        )
        entry.pack(fill="x", ipady=10, pady=(6, 0))
        entry.bind("<Return>", lambda event: self.calculate_bmi())

    @staticmethod
    def get_category(bmi):
        if bmi < 18.5:
            return "Underweight", "Below the usual adult reference range."
        elif bmi < 25:
            return "Normal weight", "Within the usual adult reference range."
        elif bmi < 30:
            return "Overweight", "Above the usual adult reference range."
        return "Obesity", "This result may be worth discussing with a healthcare professional."

    def calculate_bmi(self):
        try:
            weight = float(self.weight_var.get().strip())
            height_cm = float(self.height_var.get().strip())
            if weight <= 0 or height_cm <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Invalid input",
                "Please enter valid numbers greater than zero for weight and height."
            )
            return

        height_m = height_cm / 100
        bmi = weight / (height_m ** 2)
        category, advice = self.get_category(bmi)

        self.bmi_value.config(text=f"{bmi:.1f}")
        self.category_label.config(text=category)
        self.advice_label.config(text=advice)

    def reset(self):
        self.weight_var.set("")
        self.height_var.set("")
        self.bmi_value.config(text="—")
        self.category_label.config(text="Enter your details to begin")
        self.advice_label.config(
            text="BMI is a screening measure, not a diagnosis."
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = BMICalculatorApp(root)
    root.mainloop()
