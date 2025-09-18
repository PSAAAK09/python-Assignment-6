# calculator.py
import tkinter as tk
from tkinter import ttk, messagebox

class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tkinter Calculator")
        self.geometry("360x520")
        self.resizable(False, False)
        self._create_widgets()
        self.bind_keys()

    def _create_widgets(self):
        self.expression = ""
        self.display_var = tk.StringVar()

        # Display
        display_frame = ttk.Frame(self)
        display_frame.pack(fill="both", expand=False, padx=10, pady=(15,5))

        entry = ttk.Entry(
            display_frame,
            textvariable=self.display_var,
            font=("Helvetica", 24),
            justify="right",
            state="readonly",
            width=16
        )
        entry.pack(ipady=15, fill="x")

        # Buttons
        btns = [
            ["%", "(", ")", "C"],
            ["7", "8", "9", "⌫"],
            ["4", "5", "6", "/"],
            ["1", "2", "3", "*"],
            ["0", ".", "+", "-"],
            ["±", "=", "", ""]
        ]

        btn_frame = ttk.Frame(self)
        btn_frame.pack(padx=10, pady=10, fill="both", expand=True)

        for r, row in enumerate(btns):
            for c, label in enumerate(row):
                if not label:
                    continue
                b = ttk.Button(btn_frame, text=label, command=lambda x=label: self.on_button(x))
                b.grid(row=r, column=c, sticky="nsew", padx=4, pady=4, ipadx=6, ipady=10)
        # Grid weight
        for i in range(len(btns)):
            btn_frame.rowconfigure(i, weight=1)
        for j in range(4):
            btn_frame.columnconfigure(j, weight=1)

    def bind_keys(self):
        for key in "0123456789+-*/().%":
            self.bind(key, lambda e, k=key: self.on_button(k))
        self.bind("<Return>", lambda e: self.on_button("="))
        self.bind("<BackSpace>", lambda e: self.on_button("⌫"))
        self.bind("<Escape>", lambda e: self.on_button("C"))
        self.bind(".", lambda e: self.on_button("."))

    def on_button(self, char):
        if char == "C":
            self.expression = ""
            self.display_var.set(self.expression)
            return
        if char == "⌫":
            self.expression = self.expression[:-1]
            self.display_var.set(self.expression)
            return
        if char == "=":
            self.evaluate()
            return
        if char == "±":
            self.toggle_sign()
            return
        if char == "%":
            # percentage: convert current expression to expression/100
            try:
                val = eval(self.expression)
                self.expression = str(val / 100)
                self.display_var.set(self.expression)
            except Exception:
                self.display_var.set("Error")
                self.expression = ""
            return

        # Normal append
        self.expression += str(char)
        self.display_var.set(self.expression)

    def toggle_sign(self):
        # Simple toggle sign for the last numeric token
        if not self.expression:
            return
        try:
            # Find last number in expression
            import re
            tokens = re.split(r'([+\-*/()])', self.expression)
            if not tokens:
                return
            # Walk backwards to find a numeric token
            for i in range(len(tokens)-1, -1, -1):
                tok = tokens[i]
                if tok and (tok.replace('.', '', 1).isdigit()):
                    # toggle sign
                    num = float(tok)
                    if num == int(num):
                        new = str(int(-num))
                    else:
                        new = str(-num)
                    tokens[i] = new
                    self.expression = "".join(tokens)
                    self.display_var.set(self.expression)
                    return
        except Exception:
            pass

    def evaluate(self):
        try:
            # Safe-ish evaluation: replace unicode division / with python division
            expr = self.expression
            # Prevent accidental double-operators at end
            expr = expr.rstrip("+-*/.")
            result = eval(expr, {"__builtins__": None}, {})
            self.expression = str(result)
            self.display_var.set(self.expression)
        except ZeroDivisionError:
            messagebox.showerror("Math Error", "Division by zero is not allowed.")
            self.expression = ""
            self.display_var.set(self.expression)
        except Exception:
            messagebox.showerror("Error", "Invalid expression.")
            self.expression = ""
            self.display_var.set(self.expression)

if __name__ == "__main__":
    app = Calculator()
    app.mainloop()
