import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk  # Added for Treeview
import json
import os
from datetime import datetime

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("💸 Budget & Expense Tracker")
        self.root.geometry("700x600")
        self.budget = {}
        self.expenses = []

        self.setup_ui()

    def setup_ui(self):
        # Appearance
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.root.configure(bg="#f4f4ff")
        font_title = ("Segoe UI", 18, "bold")
        self.font_label = ("Segoe UI", 14)

        # Navigation Bar
        self.nav_frame = ctk.CTkFrame(self.root, fg_color="#3434EA")
        self.nav_frame.pack(fill="x")

        self.active_tab = ctk.StringVar(value="budget")

        nav_buttons = [("Monthly Budget", "budget"), ("Add Expense", "add"), ("Expenses", "report")]
        for label, val in nav_buttons:
            btn = ctk.CTkButton(
                self.nav_frame, text=label, width=160, height=40,
                command=lambda v=val: self.switch_tab(v),
                fg_color="#ffffff" if self.active_tab.get() == val else "#3434EA",
                text_color="#3434EA" if self.active_tab.get() == val else "white",
                hover_color="#2a2ad0",
                corner_radius=20,
                font=("Segoe UI", 14, "bold")
            )
            btn.pack(side="left", padx=10, pady=10)

        # Content Frames
        self.content_frames = {
            "budget": self.create_budget_frame(),
            "add": self.create_expense_frame(),
            "report": self.create_report_frame()
        }

        self.switch_tab("budget")

    def switch_tab(self, tab):
        self.active_tab.set(tab)
        for key, frame in self.content_frames.items():
            frame.pack_forget()
        self.content_frames[tab].pack(padx=20, pady=20, fill="both", expand=True)

        # Refresh nav colors
        for child in self.nav_frame.winfo_children():
            if isinstance(child, ctk.CTkButton):
                is_active = child.cget("text").replace(" ", "").lower() == tab
                child.configure(
                    fg_color="#ffffff" if is_active else "#3434EA",
                    text_color="#3434EA" if is_active else "white"
                )

    def create_budget_frame(self):
        frame = ctk.CTkFrame(self.root)
        ctk.CTkLabel(frame, text="Set Monthly Budget (₹)", font=("Segoe UI", 20)).pack(pady=10)

        self.budget_entries = {}
        for category in ["Food", "Travel", "Entertainment"]:
            inner_frame = ctk.CTkFrame(frame, fg_color="transparent")
            inner_frame.pack(pady=10, anchor="w")

            ctk.CTkLabel(inner_frame, text=f"{category}:", font=self.font_label).pack(side="left", padx=10)
            entry = ctk.CTkEntry(inner_frame, width=200)
            entry.pack(side="left")
            self.budget_entries[category] = entry

        ctk.CTkButton(frame, text="📂 Save Budget", command=self.save_budget, corner_radius=15, font=self.font_label).pack(pady=20)
        return frame

    def create_expense_frame(self):
        frame = ctk.CTkFrame(self.root)
        ctk.CTkLabel(frame, text="Add Expense", font=("Segoe UI", 20)).pack(pady=10)

        category_frame = ctk.CTkFrame(frame, fg_color="transparent")
        category_frame.pack(pady=5, anchor="w")
        ctk.CTkLabel(category_frame, text="Category:", font=self.font_label).pack(side="left", padx=10)
        self.expense_category = ctk.CTkComboBox(category_frame, values=["Food", "Travel", "Entertainment"], width=200)
        self.expense_category.pack(side="left")

        amount_frame = ctk.CTkFrame(frame, fg_color="transparent")
        amount_frame.pack(pady=5, anchor="w")
        ctk.CTkLabel(amount_frame, text="Amount (₹):", font=self.font_label).pack(side="left", padx=10)
        self.expense_amount = ctk.CTkEntry(amount_frame, width=200)
        self.expense_amount.pack(side="left")

        ctk.CTkButton(frame, text="➕ Add Expense", command=self.add_expense, corner_radius=15, font=self.font_label).pack(pady=20)
        return frame

    def create_report_frame(self):
        frame = ctk.CTkFrame(self.root)
        ctk.CTkLabel(frame, text="Expense Log", font=("Segoe UI", 20)).pack(pady=10)

        # Add a Treeview inside a CTkFrame for consistent appearance
        tree_style = ttk.Style()
        tree_style.configure("Treeview.Heading", font=("Segoe UI", 12, "bold"))
        tree_style.configure("Treeview", font=("Segoe UI", 11), rowheight=25)

        tree_frame = ctk.CTkFrame(frame, fg_color="transparent")
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(tree_frame, columns=("Category", "Amount", "Date"), show="headings", height=8)
        self.tree.pack(fill="both", expand=True)

        for col in ["Category", "Amount", "Date"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")

        ctk.CTkButton(frame, text="📊 Show Report & Save", command=self.save_all, corner_radius=15).pack(pady=20)
        return frame

    def save_budget(self):
        self.budget = {}
        for cat, entry in self.budget_entries.items():
            try:
                value = float(entry.get())
                self.budget[cat] = value
            except ValueError:
                messagebox.showerror("Invalid Input", f"Please enter a valid number for {cat}.")
                return
        messagebox.showinfo("Budget Saved", "✅ Budget saved successfully!")

    def add_expense(self):
        category = self.expense_category.get()
        try:
            amount = float(self.expense_amount.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid amount.")
            return

        if category not in self.budget:
            messagebox.showerror("Unknown Category", f"'{category}' is not in the budget.")
            return

        date = datetime.now().strftime("%Y-%m-%d")
        self.expenses.append({"category": category, "amount": amount, "date": date})
        self.tree.insert("", "end", values=(category, f"{amount:.2f}", date))

        self.expense_category.set("")
        self.expense_amount.delete(0, ctk.END)

    def save_all(self):
        if not self.budget:
            messagebox.showwarning("No Budget", "⚠️ Please set your monthly budget first.")
            return
        if not self.expenses:
            messagebox.showwarning("No Expenses", "⚠️ Please add at least one expense.")
            return

        month = datetime.now().strftime("%Y-%m")
        budget_file = f"{month}.json"
        expense_file = "expenditure.json"

        # Save Budget
        with open(budget_file, 'w') as f:
            json.dump(self.budget, f, indent=4)

        # Append or update Expenses
        all_expenses = {}
        if os.path.exists(expense_file):
            with open(expense_file, 'r') as f:
                all_expenses = json.load(f)

        all_expenses.setdefault(month, []).extend(self.expenses)

        with open(expense_file, 'w') as f:
            json.dump(all_expenses, f, indent=4)

        # Show Report
        self.show_report()
        self.expenses.clear()
        self.tree.delete(*self.tree.get_children())

    def show_report(self):
        spent_by_category = {}
        for entry in self.expenses:
            cat = entry["category"]
            amt = entry["amount"]
            spent_by_category[cat] = spent_by_category.get(cat, 0) + amt

        report = "📊 Expense Report:\n\n"
        for cat, spent in spent_by_category.items():
            limit = self.budget.get(cat, 0)
            diff = spent - limit
            status = "✅ WITHIN BUDGET" if diff <= 0 else f"❌ OVER by ₹{diff:.2f}"
            report += f"• {cat}: Spent ₹{spent:.2f}, Budget ₹{limit:.2f} → {status}\n"

        messagebox.showinfo("Expense Summary", report)


if __name__ == "__main__":
    root = ctk.CTk()
    app = ExpenseTrackerApp(root)
    root.mainloop()
