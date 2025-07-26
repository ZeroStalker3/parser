# Программа реализованная на CustomTkinter
# Парсинг ноутбуков с YandexMarket

import customtkinter as ctk
import threading
from main import *

ctk.set_default_color_theme("dark-blue")
ctk.set_appearance_mode("dark")

class ParserApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("💻 YandexMarket Парсер")
        self.geometry("500x400")
        self.resizable(False, False)

        ctk.CTkLabel(self, text="Парсинг ноутбуков", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)

        # Кол-во товаров
        ctk.CTkLabel(self, text="Количество товаров:").pack()
        self.entry_count = ctk.CTkEntry(self, placeholder_text="например, 50")
        self.entry_count.insert(0, "50")
        self.entry_count.pack(pady=5)

        # Минимальная и максимальная цена
        ctk.CTkLabel(self, text="Минимальная цена:").pack()
        self.entry_min_price = ctk.CTkEntry(self, placeholder_text="например, 10000")
        self.entry_min_price.insert(0, "10000")
        self.entry_min_price.pack(pady=5)

        ctk.CTkLabel(self, text="Максимальная цена:").pack()
        self.entry_max_price = ctk.CTkEntry(self, placeholder_text="например, 50000")
        self.entry_max_price.insert(0, "50000")
        self.entry_max_price.pack(pady=5)

        # Кнопка запуска парсера
        self.parse_button = ctk.CTkButton(self, text="🚀 Запустить парсинг", command=self.start_thread)
        self.parse_button.pack(pady=10)
        
        # Информационное поле
        self.output_text = ctk.CTkTextbox(self, height=200, width=450)
        self.output_text.pack(pady=10)
        self.output_text.insert("end", "Готов к работе...\n")
        self.output_text.configure(state="disabled")

    def log(self, message):
        self.output_text.configure(state="normal")
        self.output_text.insert("end", f"{message}\n")
        self.output_text.see("end")
        self.output_text.configure(state="disabled")

    def start_thread(self):
        thread = threading.Thread(target=self.run_parser_gui)
        thread.start()

    def run_parser_gui(self):
        try:
            self.log("🔍 Парсинг запущен...")
            count = int(self.entry_count.get())
            min_price = int(self.entry_min_price.get())
            max_price = int(self.entry_max_price.get())
            result = run_parser(max_items=count, min_price=min_price, max_price=max_price)
            self.log(f"✅ Завершено.")
        except Exception as e:
            self.log(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    app = ParserApp()
    app.mainloop()
