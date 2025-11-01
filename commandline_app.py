import json
import os
from datetime import datetime

class ExpenseTrackerCLI:
    def __init__(self):
        self.budget = {}
        self.expenses = []
        self.budget_file = ""
        self.expense_file = "expenditure.json"
        self.categories = ["Food", "Travel", "Entertainment"]

    def main_menu(self):
        while True:
            print("\n==== 💸 Budget & Expense Tracker ====")
            print("1. Set Monthly Budget")
            print("2. Add Expense")
            print("3. Show Expenses")
            print("4. Save & Show Report")
            print("5. Exit")
            choice = input("Choose an option (1-5): ").strip()
            if choice == '1':
                self.set_budget()
            elif choice == '2':
                self.add_expense()
            elif choice == '3':
                self.show_expenses()
            elif choice == '4':
                self.save_all()
            elif choice == '5':
                print("Exiting. Goodbye 👋")
                break
            else:
                print("Invalid choice. Please try again.")

    def set_budget(self):
        print("\n-- Set Monthly Budget --")
        for cat in self.categories:
            while True:
                try:
                    value = float(input(f"Enter budget for {cat} (₹): ").strip())
                    self.budget[cat] = value
                    break
                except ValueError:
                    print("Please enter a valid number.")
        print("✅ Budget saved successfully!")
    
    def add_expense(self):
        if not self.budget:
            print("⚠️ Please set your monthly budget first.")
            return

        print("\n-- Add Expense --")
        print("Categories:", ", ".join(self.categories))
        category = input("Enter category: ").strip().title()
        if category not in self.budget:
            print(f"'{category}' is not in the budget. Please add a valid category.")
            return
        try:
            amount = float(input("Amount (₹): ").strip())
        except ValueError:
            print("Please enter a valid amount.")
            return
        date = datetime.now().strftime("%Y-%m-%d")
        self.expenses.append({"category": category, "amount": amount, "date": date})
        print("➕ Expense added.")

    def show_expenses(self):
        print("\n-- Expense Log --")
        if not self.expenses:
            print("No expenses yet.")
            return
        print(f"{'Category':12} {'Amount':10} {'Date':12}")
        print("-" * 36)
        for exp in self.expenses:
            print(f"{exp['category']:12} {exp['amount']:10.2f} {exp['date']:12}")

    def save_all(self):
        if not self.budget:
            print("⚠️ Please set your monthly budget first.")
            return
        if not self.expenses:
            print("⚠️ Please add at least one expense.")
            return

        month = datetime.now().strftime("%Y-%m")
        self.budget_file = f"{month}.json"

        # Save budget
        with open(self.budget_file, 'w') as f:
            json.dump(self.budget, f, indent=4)
        
        # Save or append expenses
        all_expenses = {}
        if os.path.exists(self.expense_file):
            with open(self.expense_file, 'r') as f:
                all_expenses = json.load(f)

        all_expenses.setdefault(month, []).extend(self.expenses)
        with open(self.expense_file, 'w') as f:
            json.dump(all_expenses, f, indent=4)
        
        self.show_report(month)
        self.expenses.clear()

    def show_report(self, month):
        # Load expenses for the month
        with open(self.expense_file, 'r') as f:
            all_expenses = json.load(f)
        month_expenses = all_expenses.get(month, [])

        spent_by_category = {}
        for entry in month_expenses:
            cat = entry["category"]
            amt = entry["amount"]
            spent_by_category[cat] = spent_by_category.get(cat, 0) + amt

        print("\n📊 Expense Report:")
        for cat in self.categories:
            spent = spent_by_category.get(cat, 0)
            limit = self.budget.get(cat, 0)
            diff = spent - limit
            status = "✅ WITHIN BUDGET" if diff <= 0 else f"❌ OVER by ₹{diff:.2f}"
            print(f"• {cat}: Spent ₹{spent:.2f}, Budget ₹{limit:.2f} → {status}")
        print()

if __name__ == "__main__":
    app = ExpenseTrackerCLI()
    app.main_menu()
