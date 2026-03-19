import json
import os

class Expense:
    """Entity class representing a single expense record."""
    def __init__(self, category, amount, date, note):
        self.category = category
        self.amount = amount
        self.date = date
        self.note = note

class ExpenseManager:
    """Manager class to handle CRUD, search, sort, reports, and persistence."""
    def __init__(self, filename="expenses.json"):
        self.filename = filename
        self.expenses = []
        self.load_data()

    # --- CRUD ---
    def add_expense(self, category, amount, date, note):
        expense = Expense(category, amount, date, note)
        self.expenses.append(expense)
        self.save_data()

    def edit_expense(self, index, category, amount, date, note):
        if 0 <= index < len(self.expenses):
            self.expenses[index].category = category
            self.expenses[index].amount = amount
            self.expenses[index].date = date
            self.expenses[index].note = note
            self.save_data()

    def delete_expense(self, index):
        if 0 <= index < len(self.expenses):
            del self.expenses[index]
            self.save_data()

    # --- Search & Sort ---
    def search_by_category(self, category):
        return [e for e in self.expenses if e.category.lower() == category.lower()]

    def sort_by_amount(self, reverse=False):
        self.expenses.sort(key=lambda e: e.amount, reverse=reverse)

    # --- Reports ---
    def report_total(self):
        return sum(e.amount for e in self.expenses)

    def report_by_category(self):
        report = {}
        for e in self.expenses:
            report[e.category] = report.get(e.category, 0) + e.amount
        return report

    def summary(self):
        total = self.report_total()
        by_cat = self.report_by_category()
        top_category = max(by_cat, key=by_cat.get) if by_cat else None
        return {
            "total": total,
            "by_category": by_cat,
            "top_category": top_category
        }

    # --- Persistence ---
    def save_data(self):
        data = [
            {"category": e.category, "amount": e.amount, "date": e.date, "note": e.note}
            for e in self.expenses
        ]
        with open(self.filename, "w") as f:
            json.dump(data, f, indent=4)

    def load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                try:
                    data = json.load(f)
                    self.expenses = [
                        Expense(d["category"], d["amount"], d["date"], d["note"])
                        for d in data
                    ]
                except json.JSONDecodeError:
                    self.expenses = []
