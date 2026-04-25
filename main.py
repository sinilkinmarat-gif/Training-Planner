import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

# Путь к файлу данных
DATA_PATH = "data/trainings.json"

# Создаем папку data, если её нет
os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)

# Загрузка данных из JSON
def load_data():
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

# Сохранение данных в JSON
def save_data(data):
    with open(DATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Валидация даты (ГГГГ-ММ-ДД)
def validate_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

# Валидация длительности (положительное число)
def validate_duration(duration_str):
    try:
        duration = float(duration_str)
        return duration > 0
    except ValueError:
        return False

# Добавление тренировки
def add_training():
    date = entry_date.get()
    tr_type = entry_type.get()
    duration = entry_duration.get()

    if not validate_date(date):
        messagebox.showerror("Ошибка", "Дата должна быть в формате ГГГГ-ММ-ДД (например, 2026-04-25)")
        return
    if not validate_duration(duration):
        messagebox.showerror("Ошибка", "Длительность должна быть положительным числом")
        return

    training = {
        "date": date,
        "type": tr_type,
        "duration": float(duration)
    }
    trainings.append(training)
    save_data(trainings)
    update_table()
    clear_entries()

# Обновление таблицы с учетом фильтрации
def update_table():
    for i in tree.get_children():
        tree.delete(i)
    
    filter_date = entry_filter_date.get()
    filter_type = entry_filter_type.get().lower()
    
    for tr in trainings:
        date_match = (not filter_date) or (filter_date in tr["date"])
        type_match = (not filter_type) or (filter_type in tr["type"].lower())
        
        if date_match and type_match:
            tree.insert("", tk.END, values=(tr["date"], tr["type"], tr["duration"]))

# Очистка полей ввода
def clear_entries():
    entry_date.delete(0, tk.END)
    entry_type.delete(0, tk.END)
    entry_duration.delete(0, tk.END)

# Инициализация данных
trainings = load_data()

# Создание окна
root = tk.Tk()
root.title("Training Planner")
root.geometry("700x500")

# --- Поля ввода ---
frame_input = ttk.LabelFrame(root, text="Добавить тренировку", padding=(10, 5))
frame_input.pack(pady=10, fill="x")

ttk.Label(frame_input, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_date = ttk.Entry(frame_input, width=15)
entry_date.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame_input, text="Тип тренировки:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_type = ttk.Entry(frame_input, width=15)
entry_type.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(frame_input, text="Длительность (мин):").grid(row=2, column=0, padx=5, pady=5, sticky="e")
entry_duration = ttk.Entry(frame_input, width=15)
entry_duration.grid(row=2, column=1, padx=5, pady=5)

btn_add = ttk.Button(frame_input, text="Добавить тренировку", command=add_training)
btn_add.grid(row=3, columnspan=2, pady=10)


# --- Фильтрация ---
frame_filter = ttk.LabelFrame(root, text="Фильтр", padding=(10, 5))
frame_filter.pack(pady=10, fill="x")

ttk.Label(frame_filter, text="Дата:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_filter_date = ttk.Entry(frame_filter, width=15)
entry_filter_date.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame_filter, text="Тип:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_filter_type = ttk.Entry(frame_filter, width=15)
entry_filter_type.grid(row=1, column=1, padx=5, pady=5)

btn_filter = ttk.Button(frame_filter, text="Применить фильтр", command=update_table)
btn_filter.grid(row=2, columnspan=2, pady=10)


# --- Таблица ---
columns = ("Дата", "Тип", "Длительность (мин)")
tree = ttk.Treeview(root, columns=columns, show="headings", height=15)
for col in columns:
    tree.heading(col, text=col)
tree.pack(padx=10, pady=10, fill="both", expand=True)


# Запуск обновления таблицы при старте
update_table()

root.mainloop()