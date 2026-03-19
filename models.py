from datetime import datetime

class Expense:
    def __init__(self, id, category, amount, date, note=""):
        self.id = int(id)
        self.category = category.strip().capitalize()
        self.amount = float(amount)
        try:
            datetime.strptime(date, "%Y-%m-%d")
            self.date = date
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format")
        self.note = note.strip()

    def to_dict(self):
        return {
            "id": self.id,
            "category": self.category,
            "amount": self.amount,
            "date": self.date,
            "note": self.note
        }

    def __repr__(self):
        return f"Expense(id={self.id}, category='{self.category}', amount={self.amount}, date='{self.date}', note='{self.note}')"
