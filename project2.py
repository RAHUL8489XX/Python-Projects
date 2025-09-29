import sqlite3
import datetime
import matplotlib.pyplot as plt
from typing import List, Tuple

class FinanceTracker:
    def __init__(self, db_name='finance.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()
    
    def create_tables(self):
        """Create database tables if they don't exist"""
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                type TEXT NOT NULL,
                category TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT
            )
        ''')
        self.conn.commit()
    
    def add_transaction(self, trans_type: str, category: str, 
                       amount: float, description: str = ""):
        """Add income or expense transaction"""
        date = datetime.date.today().isoformat()
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO transactions (date, type, category, amount, description)
            VALUES (?, ?, ?, ?, ?)
        ''', (date, trans_type, category, amount, description))
        self.conn.commit()
        print(f"✓ {trans_type.capitalize()} of ${amount:.2f} added to {category}")
    
    def get_balance(self) -> float:
        """Calculate current balance"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT type, amount FROM transactions')
        transactions = cursor.fetchall()
        
        balance = 0
        for trans_type, amount in transactions:
            if trans_type == 'income':
                balance += amount
            else:
                balance -= amount
        return balance
    
    def get_summary(self, month: int = None, year: int = None):
        """Get financial summary"""
        cursor = self.conn.cursor()
        
        if month and year:
            date_filter = f"{year}-{month:02d}%"
            cursor.execute('''
                SELECT type, category, SUM(amount)
                FROM transactions
                WHERE date LIKE ?
                GROUP BY type, category
            ''', (date_filter,))
        else:
            cursor.execute('''
                SELECT type, category, SUM(amount)
                FROM transactions
                GROUP BY type, category
            ''')
        
        results = cursor.fetchall()
        
        income_by_category = {}
        expense_by_category = {}
        
        for trans_type, category, total in results:
            if trans_type == 'income':
                income_by_category[category] = total
            else:
                expense_by_category[category] = total
        
        total_income = sum(income_by_category.values())
        total_expenses = sum(expense_by_category.values())
        
        print("\n=== FINANCIAL SUMMARY ===")
        print(f"Total Income: ${total_income:.2f}")
        print(f"Total Expenses: ${total_expenses:.2f}")
        print(f"Net Savings: ${total_income - total_expenses:.2f}")
        print(f"Current Balance: ${self.get_balance():.2f}")
        
        print("\nIncome by Category:")
        for cat, amt in income_by_category.items():
            print(f"  {cat}: ${amt:.2f}")
        
        print("\nExpenses by Category:")
        for cat, amt in expense_by_category.items():
            print(f"  {cat}: ${amt:.2f}")
        
        return expense_by_category
    
    def visualize_expenses(self, expense_data: dict):
        """Create pie chart of expenses"""
        if not expense_data:
            print("No expense data to visualize")
            return
        
        plt.figure(figsize=(10, 7))
        plt.pie(expense_data.values(), labels=expense_data.keys(), 
                autopct='%1.1f%%', startangle=90)
        plt.title('Expenses by Category')
        plt.axis('equal')
        plt.savefig('expense_breakdown.png')
        print("\nChart saved as 'expense_breakdown.png'")
    
    def view_transactions(self, limit: int = 10):
        """View recent transactions"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT date, type, category, amount, description
            FROM transactions
            ORDER BY date DESC
            LIMIT ?
        ''', (limit,))
        
        transactions = cursor.fetchall()
        
        print(f"\n=== RECENT {limit} TRANSACTIONS ===")
        for date, trans_type, category, amount, desc in transactions:
            symbol = "+" if trans_type == "income" else "-"
            print(f"{date} | {symbol}${amount:.2f} | {category} | {desc}")
    
    def delete_transaction(self, transaction_id: int):
        """Delete a transaction by ID"""
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM transactions WHERE id = ?', (transaction_id,))
        self.conn.commit()
        print(f"✓ Transaction {transaction_id} deleted")
    
    def close(self):
        """Close database connection"""
        self.conn.close()


def main():
    """Main menu for the finance tracker"""
    tracker = FinanceTracker()
    
    while True:
        print("\n" + "="*40)
        print("PERSONAL FINANCE TRACKER")
        print("="*40)
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Summary")
        print("4. View Recent Transactions")
        print("5. Generate Chart")
        print("6. Exit")
        print("="*40)
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == '1':
            category = input("Category (e.g., Salary, Freelance): ")
            amount = float(input("Amount: $"))
            description = input("Description (optional): ")
            tracker.add_transaction('income', category, amount, description)
        
        elif choice == '2':
            category = input("Category (e.g., Rent, Food, Transport): ")
            amount = float(input("Amount: $"))
            description = input("Description (optional): ")
            tracker.add_transaction('expense', category, amount, description)
        
        elif choice == '3':
            expense_data = tracker.get_summary()
        
        elif choice == '4':
            limit = input("How many transactions to show? (default 10): ")
            limit = int(limit) if limit else 10
            tracker.view_transactions(limit)
        
        elif choice == '5':
            expense_data = tracker.get_summary()
            tracker.visualize_expenses(expense_data)
        
        elif choice == '6':
            print("\nGoodbye! Your data is saved in 'finance.db'")
            tracker.close()
            break
        
        else:
            print("Invalid choice! Please try again.")


# Demo mode - uncomment to run with sample data
def demo():
    """Run demo with sample transactions"""
    tracker = FinanceTracker()
    
    # Sample transactions
    tracker.add_transaction('income', 'Salary', 3000, 'Monthly salary')
    tracker.add_transaction('expense', 'Rent', 1000, 'Monthly rent')
    tracker.add_transaction('expense', 'Food', 300, 'Groceries')
    tracker.add_transaction('expense', 'Transport', 150, 'Gas and metro')
    tracker.add_transaction('expense', 'Entertainment', 100, 'Movies and games')
    tracker.add_transaction('income', 'Freelance', 500, 'Side project')
    
    # Generate report
    expense_data = tracker.get_summary()
    tracker.visualize_expenses(expense_data)
    tracker.view_transactions()
    
    tracker.close()


if __name__ == "__main__":
    # Run interactive mode
    main()
    
    # Or run demo mode (uncomment below)
    # demo()