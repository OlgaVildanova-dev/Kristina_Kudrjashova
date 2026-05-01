import tkinter as tk
from tkinter import messagebox, ttk
import random
import json
import os

# --- Настройки ---
DATA_FILE = "quotes.json"
DEFAULT_QUOTES = [
    {"text": "Жизнь — это то, что происходит, пока ты строишь другие планы.", "author": "Джон Леннон", "theme": "жизнь"},
    {"text": "Будь тем изменением, которое ты хочешь видеть в мире.", "author": "Махатма Ганди", "theme": "мотивация"},
    {"text": "Единственный способ сделать что-то хорошо — любить то, что ты делаешь.", "author": "Стив Джобс", "theme": "работа"},
]

# --- Загрузка данных ---
def load_quotes():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return DEFAULT_QUOTES.copy()

def save_quotes(quotes):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(quotes, f, ensure_ascii=False, indent=2)

# --- Основная логика ---
class QuoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор случайных цитат")
        self.root.geometry("600x500")

        self.quotes = load_quotes()
        self.history = []

        self.create_widgets()
        self.update_history_list()

    def create_widgets(self):
        # Текущая цитата
        self.quote_label = tk.Label(self.root, text="", wraplength=500, font=('Arial', 12), justify='left')
        self.quote_label.pack(pady=10)

        self.author_label = tk.Label(self.root, text="", font=('Arial', 10, 'italic'))
        self.author_label.pack()

        # Кнопка генерации
        self.generate_btn = tk.Button(self.root, text="Сгенерировать цитату", command=self.generate_quote)
        self.generate_btn.pack(pady=5)

        # Фильтры
        filter_frame = tk.Frame(self.root)
        filter_frame.pack(pady=5)

        tk.Label(filter_frame, text="Фильтр по автору:").pack(side=tk.LEFT)
        self.author_filter = tk.Entry(filter_frame)
        self.author_filter.pack(side=tk.LEFT, padx=5)

        tk.Label(filter_frame, text="Тема:").pack(side=tk.LEFT)
        self.theme_filter = ttk.Combobox(filter_frame, values=self.get_unique_themes())
        self.theme_filter.pack(side=tk.LEFT, padx=5)

        self.filter_btn = tk.Button(filter_frame, text="Применить фильтр", command=self.apply_filter)
        self.filter_btn.pack(side=tk.LEFT, padx=5)

        # История
        history_frame = tk.Frame(self.root)
        history_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        tk.Label(history_frame, text="История сгенерированных цитат:").pack()
        self.history_listbox = tk.Listbox(history_frame, height=10)
        self.history_listbox.pack(fill=tk.BOTH, expand=True)

    def get_unique_themes(self):
        return sorted(set(q["theme"] for q in self.quotes))

    def generate_quote(self):
        if not self.quotes:
            messagebox.showwarning("Нет цитат", "База цитат пуста.")
            return

        quote = random.choice(self.quotes)
        self.quote_label.config(text=f'"{quote["text"]}"')
        self.author_label.config(text=f"— {quote['author']}")

        # Добавляем в историю (без повторов)
        entry = f'"{quote["text"]}" — {quote["author"]}'
        if entry not in self.history:
            self.history.append(entry)
            self.history_listbox.insert(0, entry)
            save_quotes(self.quotes)  # Сохраняем изменения (если были добавления)

    def apply_filter(self):
        author = self.author_filter.get().strip().lower()
        theme = self.theme_filter.get().strip().lower()

        filtered = [
            q for q in self.quotes
            if (not author or author in q["author"].lower())
            and (not theme or theme == q["theme"].lower())
        ]

        if not filtered:
            messagebox.showinfo("Фильтр", "Нет цитат по заданным критериям.")
            return

        quote = random.choice(filtered)
        self.quote_label.config(text=f'"{quote["text"]}"')
        self.author_label.config(text=f"— {quote['author']}")

    def update_history_list(self):
        self.history_listbox.delete(0, tk.END)
        for entry in self.history:
            self.history_listbox.insert(tk.END, entry)

if __name__ == "__main__":
    root = tk.Tk()
    app = QuoteApp(root)
    root.mainloop()
