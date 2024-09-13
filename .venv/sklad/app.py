import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime

class Product:
    """Класс продукта"""
    def __init__(self, name, brand, quantity, price, weight, unit, expiration_from, expiration_to):
        self.name = name
        self.brand = brand
        self.quantity = quantity
        self.price = price
        self.weight = weight
        self.unit = unit
        self.expiration_from = expiration_from
        self.expiration_to = expiration_to

    def __str__(self):
        return f'{self.name} ({self.brand}): {self.quantity} шт., цена: {self.price} руб., вес: {self.weight} {self.unit}, срок годности: от {self.expiration_from} до {self.expiration_to}'

    def get_expiration_period(self):
        """Получить строку с датами срока годности"""
        return f"от {self.expiration_from} до {self.expiration_to}"

class Warehouse:
    """Класс склада"""
    def __init__(self):
        self.products = {}

    def add_product(self, category, name, brand, quantity, price, weight, unit, expiration_from, expiration_to):
        """Добавить продукт на склад по категориям"""
        if category not in self.products:
            self.products[category] = {}

        if name in self.products[category]:
            self.products[category][name].quantity += quantity
        else:
            self.products[category][name] = Product(name, brand, quantity, price, weight, unit, expiration_from, expiration_to)

    def update_product(self, category, old_name, name, brand, quantity, price, weight, unit, expiration_from, expiration_to):
        """Обновить продукт на складе"""
        if category in self.products and old_name in self.products[category]:
            del self.products[category][old_name]
            self.add_product(category, name, brand, quantity, price, weight, unit, expiration_from, expiration_to)

    def remove_product(self, category, name):
        """Удалить продукт со склада по категориям"""
        if category in self.products and name in self.products[category]:
            del self.products[category][name]
            return True
        else:
            return False

    def get_products(self, category):
        """Получить список продуктов по категориям"""
        if category in self.products:
            return [(product.name, product.brand, product.quantity, product.price, f"{product.weight} {product.unit}", product.get_expiration_period()) for product in self.products[category].values()]
        else:
            return []

class WarehouseApp:
    """Графическое приложение для управления складом"""
    def __init__(self, root):
        self.warehouse = Warehouse()

        self.root = root
        self.root.title("Продуктовый склад")
        self.root.geometry("900x600")

        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.notebook = ttk.Notebook(root)
        self.notebook.grid(row=0, column=0, sticky='nsew')

        self.fruits_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.fruits_tab, text="Фрукты")

        self.vegetables_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.vegetables_tab, text="Овощи")

        self.drinks_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.drinks_tab, text="Напитки")

        self.create_tab_interface(self.fruits_tab, "1ый Раздел")
        self.create_tab_interface(self.vegetables_tab, "2ой Раздел")
        self.create_tab_interface(self.drinks_tab, "3ий Раздел")

    def create_tab_interface(self, tab, category_name):
        """Создать интерфейс для каждой вкладки"""

        add_button = ttk.Button(tab, text="Добавить продукт", command=lambda: self.open_add_product_window(category_name))
        add_button.grid(row=0, column=0, padx=10, pady=5, sticky='w')

        edit_button = ttk.Button(tab, text="Редактировать продукт", command=lambda: self.edit_selected_product(category_name, product_tree))
        edit_button.grid(row=0, column=1, padx=10, pady=5, sticky='w')

        remove_button = ttk.Button(tab, text="Удалить продукт", command=lambda: self.remove_selected_product(category_name, product_tree))
        remove_button.grid(row=0, column=2, padx=10, pady=5, sticky='w')

        product_tree = ttk.Treeview(tab, columns=("name", "brand", "quantity", "price", "weight", "expiration"), show="headings", height=10)
        product_tree.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        product_tree.heading("name", text="Название")
        product_tree.heading("brand", text="Бренд")
        product_tree.heading("quantity", text="Количество")
        product_tree.heading("price", text="Цена (руб)")
        product_tree.heading("weight", text="Вес")
        product_tree.heading("expiration", text="Срок годности")

        product_tree.column("name", width=150)
        product_tree.column("brand", width=100)
        product_tree.column("quantity", width=100)
        product_tree.column("price", width=100)
        product_tree.column("weight", width=150)
        product_tree.column("expiration", width=200)

        tab.grid_rowconfigure(1, weight=1)
        tab.grid_columnconfigure(1, weight=1)

        setattr(self, f'{category_name.lower()}_tree', product_tree)
        self.update_product_tree(category_name, product_tree)

    def open_add_product_window(self, category_name):
        """Открыть новое окно для добавления продукта"""
        self.open_product_window(category_name, is_edit=False)

    def open_product_window(self, category_name, is_edit=False, old_product_info=None):
        """Открыть окно для добавления или редактирования продукта"""
        title = "Редактировать продукт" if is_edit else "Добавить продукт"
        product_window = tk.Toplevel(self.root)
        product_window.title(f"{title} в {category_name}")
        product_window.geometry("550x300")

        name_label = ttk.Label(product_window, text="Название продукта:")
        name_label.grid(row=0, column=0, padx=10, pady=5)
        name_entry = ttk.Entry(product_window)
        name_entry.grid(row=0, column=1, padx=10, pady=5)

        brand_label = ttk.Label(product_window, text="Бренд:")
        brand_label.grid(row=1, column=0, padx=10, pady=5)
        brand_entry = ttk.Entry(product_window)
        brand_entry.grid(row=1, column=1, padx=10, pady=5)

        quantity_label = ttk.Label(product_window, text="Количество:")
        quantity_label.grid(row=2, column=0, padx=10, pady=5)
        quantity_entry = ttk.Entry(product_window)
        quantity_entry.grid(row=2, column=1, padx=10, pady=5)

        price_label = ttk.Label(product_window, text="Цена (руб):")
        price_label.grid(row=3, column=0, padx=10, pady=5)
        price_entry = ttk.Entry(product_window)
        price_entry.grid(row=3, column=1, padx=10, pady=5)

        weight_label = ttk.Label(product_window, text="Вес:")
        weight_label.grid(row=4, column=0, padx=10, pady=5)
        weight_entry = ttk.Entry(product_window)
        weight_entry.grid(row=4, column=1, padx=10, pady=5)

        unit_var = tk.StringVar()
        unit_combobox = ttk.Combobox(product_window, textvariable=unit_var, values=["Г", "КГ", "Л"], state="readonly")
        unit_combobox.grid(row=4, column=2, padx=10, pady=5)

        expiration_from_label = ttk.Label(product_window, text="Срок от (ДД-ММ-ГГГГ):")
        expiration_from_label.grid(row=5, column=0, padx=10, pady=5)
        expiration_from_entry = ttk.Entry(product_window)
        expiration_from_entry.grid(row=5, column=1, padx=10, pady=5)

        expiration_to_label = ttk.Label(product_window, text="Срок до (ДД-ММ-ГГГГ):")
        expiration_to_label.grid(row=6, column=0, padx=10, pady=5)
        expiration_to_entry = ttk.Entry(product_window)
        expiration_to_entry.grid(row=6, column=1, padx=10, pady=5)

        if is_edit and old_product_info:
            name_entry.insert(0, old_product_info[0])
            brand_entry.insert(0, old_product_info[1])
            quantity_entry.insert(0, old_product_info[2])
            price_entry.insert(0, old_product_info[3])
            weight_entry.insert(0, old_product_info[4].split()[0])  # Только значение веса
            unit_combobox.set(old_product_info[4].split()[1])  # Устанавливаем единицу измерения
            expiration_from_entry.insert(0, old_product_info[5].split(" до ")[0].replace("от ", ""))
            expiration_to_entry.insert(0, old_product_info[5].split(" до ")[1])

        save_button = ttk.Button(product_window, text="Сохранить", command=lambda: self.save_product(category_name, name_entry, brand_entry, quantity_entry, price_entry, weight_entry, unit_var, expiration_from_entry, expiration_to_entry, product_window, is_edit, old_product_info))
        save_button.grid(row=7, column=0, columnspan=3, padx=10, pady=10)

    def save_product(self, category, name_entry, brand_entry, quantity_entry, price_entry, weight_entry, unit_var, expiration_from_entry, expiration_to_entry, product_window, is_edit, old_product_info):
        """Сохранить продукт (добавить или обновить)"""
        name = name_entry.get()
        brand = brand_entry.get()
        quantity = int(quantity_entry.get())
        price = float(price_entry.get())
        weight = float(weight_entry.get())
        unit = unit_var.get()
        expiration_from = expiration_from_entry.get()
        expiration_to = expiration_to_entry.get()

        try:
            expiration_from_dt = datetime.strptime(expiration_from, "%d-%m-%Y")
            expiration_to_dt = datetime.strptime(expiration_to, "%d-%m-%Y")

            if expiration_from_dt >= expiration_to_dt:
                messagebox.showerror("Ошибка", "Дата начала срока годности должна быть раньше даты окончания.")
                return
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты. Используйте ДД-ММ-ГГГГ.")
            return

        if is_edit:
            old_name = old_product_info[0]
            self.warehouse.update_product(category, old_name, name, brand, quantity, price, weight, unit, expiration_from, expiration_to)
        else:
            self.warehouse.add_product(category, name, brand, quantity, price, weight, unit, expiration_from, expiration_to)

        product_window.destroy()
        self.update_product_tree(category, getattr(self, f"{category.lower()}_tree"))

    def update_product_tree(self, category, tree):
        """Обновить дерево продуктов для категории"""
        for item in tree.get_children():
            tree.delete(item)

        for product in self.warehouse.get_products(category):
            tree.insert("", "end", values=product)

    def edit_selected_product(self, category, tree):
        """Редактировать выбранный продукт"""
        selected_item = tree.selection()

        if selected_item:
            product_info = tree.item(selected_item, "values")
            self.open_product_window(category, is_edit=True, old_product_info=product_info)
        else:
            messagebox.showwarning("Предупреждение", "Выберите продукт для редактирования.")

    def remove_selected_product(self, category, tree):
        """Удалить выбранный продукт"""
        selected_item = tree.selection()

        if selected_item:
            product_info = tree.item(selected_item, "values")
            confirm = messagebox.askyesno("Подтверждение", f"Вы уверены, что хотите удалить продукт '{product_info[0]}'?")
            if confirm:
                self.warehouse.remove_product(category, product_info[0])
                self.update_product_tree(category, tree)
        else:
            messagebox.showwarning("Предупреждение", "Выберите продукт для удаления.")


if __name__ == "__main__":
    root = tk.Tk()
    app = WarehouseApp(root)
    root.mainloop()
