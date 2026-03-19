import customtkinter as ctk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
import matplotlib.pyplot as plt


class ExpenseApp(ctk.CTk):

    def __init__(self, manager):
        super().__init__()

        self.manager = manager

        self.title("Expense Tracker")
        self.geometry("1100x700")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # ---------------- HEADER ----------------

        header = ctk.CTkLabel(
            self,
            text="💰 Expense Management System",
            font=("Segoe UI", 34, "bold")
        )
        header.pack(pady=(20, 5))

        subheader = ctk.CTkLabel(
            self,
            text="Track • Analyze • Visualize",
            font=("Segoe UI", 16),
            text_color="gray"
        )
        subheader.pack(pady=(0, 15))

        # ---------------- MIDDLE FRAME ----------------

        middle_frame = ctk.CTkFrame(self, corner_radius=15)
        middle_frame.pack(pady=10, fill="x", padx=20)

        # ---------------- INPUT FRAME ----------------

        input_frame = ctk.CTkFrame(middle_frame, corner_radius=10)
        input_frame.pack(side="left", padx=20, pady=20)

        self.category_entry = ctk.CTkEntry(input_frame, placeholder_text="Category")
        self.category_entry.pack(pady=8, padx=10)

        self.amount_entry = ctk.CTkEntry(input_frame, placeholder_text="Amount")
        self.amount_entry.pack(pady=8, padx=10)

        self.date_entry = DateEntry(input_frame, width=20)
        self.date_entry.pack(pady=8, padx=10)

        self.note_entry = ctk.CTkEntry(input_frame, placeholder_text="Note")
        self.note_entry.pack(pady=8, padx=10)

        # ---------------- SUMMARY DASHBOARD ----------------

        summary_frame = ctk.CTkFrame(middle_frame, corner_radius=15)
        summary_frame.pack(side="right", padx=20, pady=20)

        self.total_label = ctk.CTkLabel(
            summary_frame,
            text="Total Expense\n0",
            font=("Segoe UI", 18, "bold")
        )
        self.total_label.pack(pady=15, padx=20)

        self.top_label = ctk.CTkLabel(
            summary_frame,
            text="Top Category\nNone",
            font=("Segoe UI", 18, "bold")
        )
        self.top_label.pack(pady=15, padx=20)

        self.last_label = ctk.CTkLabel(
            summary_frame,
            text="Last Expense\nNone",
            font=("Segoe UI", 18, "bold")
        )
        self.last_label.pack(pady=15, padx=20)

        

        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=15)

        ctk.CTkButton(button_frame, text="➕ Add", fg_color="#00C853", command=self.add_expense).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="✏ Edit", fg_color="#2979FF", command=self.edit_expense).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="🗑 Delete", fg_color="#D50000", command=self.delete_expense).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="🔍 Search", fg_color="#455A64", command=self.search_expense).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Sort ↑", command=lambda: self.sort_expense(False)).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Sort ↓", command=lambda: self.sort_expense(True)).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="📊 Summary", fg_color="#6A1B9A", command=self.show_summary).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="🥧 Pie Chart", fg_color="#FF6D00", command=self.show_chart).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="📈 Bar Chart", fg_color="#009688", command=self.show_bar_chart).pack(side="left", padx=5)

        # ---------------- TABLE ----------------

        style = ttk.Style()
        style.theme_use("default")

        style.configure(
            "Treeview",
            background="#1e1e1e",
            foreground="white",
            rowheight=28,
            fieldbackground="#1e1e1e"
        )

        style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 12, "bold")
        )

        self.tree = ttk.Treeview(self, columns=("Serial", "Category", "Amount", "Date", "Note"), show="headings")

        for col in ("Serial", "Category", "Amount", "Date", "Note"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=180, anchor="center")

        self.tree.pack(pady=10, fill="both", expand=True, padx=20)

        self.refresh_list()
        self.update_summary()

    

    def add_expense(self):
        try:
            category = self.category_entry.get()
            amount = float(self.amount_entry.get())
            date = self.date_entry.get_date().strftime("%Y-%m-%d")
            note = self.note_entry.get()

            if not category:
                raise ValueError("Category required")

            self.manager.add_expense(category, amount, date, note)

            messagebox.showinfo("Success", "Expense added successfully")

            self.refresh_list()
            self.update_summary()

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def edit_expense(self):

        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning("Warning", "Select an expense to edit")
            return

        index = self.tree.index(selected[0])

        category = self.category_entry.get()

        try:
            amount = float(self.amount_entry.get())
        except:
            messagebox.showerror("Error", "Invalid amount")
            return

        date = self.date_entry.get_date().strftime("%Y-%m-%d")
        note = self.note_entry.get()

        self.manager.edit_expense(index, category, amount, date, note)

        messagebox.showinfo("Success", "Expense updated")

        self.refresh_list()
        self.update_summary()

    def delete_expense(self):

        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning("Warning", "Select an expense")
            return

        index = self.tree.index(selected[0])

        self.manager.delete_expense(index)

        messagebox.showinfo("Success", "Expense deleted")

        self.refresh_list()
        self.update_summary()

    

    def search_expense(self):

        category = self.category_entry.get()

        results = self.manager.search_by_category(category)

        for row in self.tree.get_children():
            self.tree.delete(row)

        serial = 1

        for e in results:
            self.tree.insert("", "end", values=(serial, e.category, e.amount, e.date, e.note))
            serial += 1

    def sort_expense(self, reverse=False):

        self.manager.sort_by_amount(reverse)

        self.refresh_list()

    
    def show_summary(self):

        summary = self.manager.summary()

        text = f"Total Expense: {summary['total']}\nTop Category: {summary['top_category']}\n\nBy Category:\n"

        for cat, amt in summary["by_category"].items():
            text += f"{cat}: {amt}\n"

        messagebox.showinfo("Summary", text)

        self.update_summary()

    def show_chart(self):

        data = self.manager.report_by_category()

        categories = list(data.keys())
        amounts = list(data.values())

        if not categories:
            messagebox.showwarning("No Data", "No expenses available")
            return

        plt.figure(figsize=(6, 6))
        plt.pie(amounts, labels=categories, autopct="%1.1f%%")
        plt.title("Expenses by Category")
        plt.show()

    def show_bar_chart(self):

        expenses = self.manager.expenses

        if not expenses:
            messagebox.showwarning("No Data", "No expenses available")
            return

        monthly = {}

        for e in expenses:
            month = e.date[:7]
            monthly[month] = monthly.get(month, 0) + e.amount

        months = list(monthly.keys())
        amounts = list(monthly.values())

        plt.figure(figsize=(8, 5))
        plt.bar(months, amounts)
        plt.title("Monthly Expense Trend")
        plt.xlabel("Month")
        plt.ylabel("Amount")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    

    def refresh_list(self):

        for row in self.tree.get_children():
            self.tree.delete(row)

        serial = 1

        for e in self.manager.expenses:
            self.tree.insert("", "end", values=(serial, e.category, e.amount, e.date, e.note))
            serial += 1

    def update_summary(self):

        summary = self.manager.summary()

        self.total_label.configure(text=f"💵 Total Expense\n{summary['total']}")

        self.top_label.configure(text=f"🏆 Top Category\n{summary['top_category']}")

        if self.manager.expenses:
            last = self.manager.expenses[-1].date
            self.last_label.configure(text=f"📅 Last Expense\n{last}")
        else:
            self.last_label.configure(text="📅 Last Expense\nNone")