import customtkinter as ctk
import requests

# ------------------ Calculator Logic ------------------
class CalculatorLogic:
    def __init__(self):
        self.expression = ""

    def add_to_expression(self, value):
        self.expression += str(value)

    def clear(self):
        self.expression = ""

    def calculate(self):
        try:
            result = str(eval(self.expression))
            self.expression = result
            return result
        except Exception:
            self.expression = ""
            return "Error"


# ------------------ Currency Converter ------------------
class CurrencyConverter:
    def __init__(self):
        self.api_url = "https://open.er-api.com/v6/latest/USD"
        self.rates = self.load_rates()

    def load_rates(self):
        try:
            response = requests.get(self.api_url, timeout=3)
            data = response.json()
            return data["rates"]
        except Exception:
            # fallback if internet unavailable
            return {
                "USD": 1, "PKR": 280.0, "EUR": 0.91, "GBP": 0.78,
                "INR": 83.2, "AED": 3.67, "SAR": 3.75, "CAD": 1.36,
                "AUD": 1.52, "JPY": 150.5, "CNY": 7.2, "TRY": 33.5,
                "KWD": 0.31, "BDT": 118.0, "CHF": 0.89
            }

    def convert(self, amount, from_currency, to_currency):
        try:
            if from_currency not in self.rates or to_currency not in self.rates:
                return "Invalid currency"
            usd_amount = amount / self.rates[from_currency]
            converted = usd_amount * self.rates[to_currency]
            return round(converted, 2)
        except Exception:
            return "Error"


# ------------------ Main App ------------------
class ModernCalculatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.logic = CalculatorLogic()
        self.converter = CurrencyConverter()

        self.title("💎 Modern Calculator + Converter + Discount Tool")
        self.geometry("400x620")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.configure(bg="#1E1E1E")

        # Tabs
        self.tabview = ctk.CTkTabview(self, width=380, height=580)
        self.tabview.pack(pady=10, padx=10, fill="both", expand=True)

        self.calc_tab = self.tabview.add("Calculator")
        self.currency_tab = self.tabview.add("Currency")
        self.discount_tab = self.tabview.add("Discount")

        self.build_calculator_ui()
        self.build_currency_ui()
        self.build_discount_ui()

    # -------------- Calculator UI --------------
    def build_calculator_ui(self):
        self.entry = ctk.CTkEntry(
            self.calc_tab, font=("Segoe UI", 24), justify="right", width=340, height=60
        )
        self.entry.pack(pady=15)

        button_colors = {
            "numbers": "#2C2C2E",
            "operator": "#FF9500",
            "equal": "#34C759",
            "clear": "#FF3B30"
        }

        buttons = [
            ("7", button_colors["numbers"]), ("8", button_colors["numbers"]), ("9", button_colors["numbers"]), ("/", button_colors["operator"]),
            ("4", button_colors["numbers"]), ("5", button_colors["numbers"]), ("6", button_colors["numbers"]), ("*", button_colors["operator"]),
            ("1", button_colors["numbers"]), ("2", button_colors["numbers"]), ("3", button_colors["numbers"]), ("-", button_colors["operator"]),
            ("0", button_colors["numbers"]), (".", button_colors["numbers"]), ("=", button_colors["equal"]), ("+", button_colors["operator"])
        ]

        frame = ctk.CTkFrame(self.calc_tab, fg_color="#1E1E1E")
        frame.pack(pady=10)

        row, col = 0, 0
        for text, color in buttons:
            btn = ctk.CTkButton(
                frame, text=text, width=70, height=60, corner_radius=10,
                fg_color=color, hover_color="#3A3A3C" if color == button_colors["numbers"] else None,
                text_color="white", font=("Segoe UI", 18, "bold"),
                command=lambda val=text: self.on_button_click(val)
            )
            btn.grid(row=row, column=col, padx=5, pady=5)
            col += 1
            if col > 3:
                col = 0
                row += 1

        clear_btn = ctk.CTkButton(
            self.calc_tab, text="Clear", fg_color=button_colors["clear"],
            width=340, height=45, text_color="white",
            font=("Segoe UI", 16, "bold"), command=self.clear
        )
        clear_btn.pack(pady=5)

    def on_button_click(self, char):
        if char == "=":
            result = self.logic.calculate()
            self.entry.delete(0, "end")
            self.entry.insert("end", result)
        else:
            self.logic.add_to_expression(char)
            self.entry.delete(0, "end")
            self.entry.insert("end", self.logic.expression)

    def clear(self):
        self.logic.clear()
        self.entry.delete(0, "end")

    # -------------- Currency UI --------------
    def build_currency_ui(self):
        ctk.CTkLabel(self.currency_tab, text="Currency Converter", font=("Segoe UI", 22, "bold")).pack(pady=10)

        self.amount_entry = ctk.CTkEntry(self.currency_tab, placeholder_text="Enter amount", width=300, height=40)
        self.amount_entry.pack(pady=10)

        currencies = ["USD", "PKR", "EUR", "GBP", "INR", "AED", "SAR", "CAD",
                      "AUD", "JPY", "CNY", "TRY", "KWD", "BDT", "POUND"]

        self.from_currency = ctk.CTkOptionMenu(self.currency_tab, values=currencies, width=130)
        self.to_currency = ctk.CTkOptionMenu(self.currency_tab, values=currencies, width=130)

        self.from_currency.set("USD")
        self.to_currency.set("PKR")

        self.from_currency.pack(pady=5)
        self.to_currency.pack(pady=5)

        convert_btn = ctk.CTkButton(
            self.currency_tab, text="Convert", fg_color="#1E90FF",
            width=300, height=45, text_color="white",
            font=("Segoe UI", 16, "bold"), command=self.convert_currency
        )
        convert_btn.pack(pady=15)

        self.result_label = ctk.CTkLabel(self.currency_tab, text="", font=("Segoe UI", 18))
        self.result_label.pack(pady=10)

    def convert_currency(self):
        try:
            amount = float(self.amount_entry.get())
            from_curr = self.from_currency.get()
            to_curr = self.to_currency.get()

            result = self.converter.convert(amount, from_curr, to_curr)
            self.result_label.configure(text=f"{amount} {from_curr} = {result} {to_curr}")
        except ValueError:
            self.result_label.configure(text="Please enter a valid number")

    # -------------- Discount Calculator --------------
    def build_discount_ui(self):
        ctk.CTkLabel(self.discount_tab, text="Discount Calculator", font=("Segoe UI", 22, "bold")).pack(pady=10)

        self.price_entry = ctk.CTkEntry(self.discount_tab, placeholder_text="Original Price", width=300, height=40)
        self.price_entry.pack(pady=8)

        self.discount_entry = ctk.CTkEntry(self.discount_tab, placeholder_text="Discount (%)", width=300, height=40)
        self.discount_entry.pack(pady=8)

        calc_btn = ctk.CTkButton(
            self.discount_tab, text="Calculate Discount", fg_color="#34C759",
            width=300, height=45, text_color="white", font=("Segoe UI", 16, "bold"),
            command=self.calculate_discount
        )
        calc_btn.pack(pady=15)

        self.discount_result = ctk.CTkLabel(self.discount_tab, text="", font=("Segoe UI", 18))
        self.discount_result.pack(pady=10)

    def calculate_discount(self):
        try:
            price = float(self.price_entry.get())
            discount_percent = float(self.discount_entry.get())

            if price < 0 or discount_percent < 0:
                self.discount_result.configure(text="❌ Values cannot be negative")
                return

            if discount_percent > 100:
                self.discount_result.configure(text="❌ Discount cannot exceed 100%")
                return

            savings = (price * discount_percent) / 100
            final_price = price - savings

            self.discount_result.configure(
                text=f"💰 Final Price: {final_price:.2f}\n🎯 You Save: {savings:.2f}"
            )

        except ValueError:
            self.discount_result.configure(text="Please enter valid numbers")


# ------------------ Run App ------------------
if __name__ == "__main__":
    app = ModernCalculatorApp()
    app.mainloop()
