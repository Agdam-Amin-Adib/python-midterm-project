from manager import ExpenseManager
from ui import ExpenseApp

def main():
    manager = ExpenseManager("expenses.json")
    app = ExpenseApp(manager)
    app.mainloop()

if __name__ == "__main__":
    main()
