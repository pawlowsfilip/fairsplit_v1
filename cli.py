import os
import sys
from data_manager import DataManager

class CLI:
    def __init__(self):
        self.data_manager = DataManager()

    def clear_console(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def pause_and_clear(self):
        input("\nPress Enter to continue...")
        self.clear_console()

    def display_menu(self):
        print("\nWelcome to FairSplit")
        print("1. Create a Group")
        print("2. Add Expense to Group")
        print("3. View Group Balances")
        print("4. Settle Debts")
        print("5. Record Payment")
        print("6. Help")
        print("7. Exit")

    def run(self):
        while True:
            self.display_menu()
            choice = input("\nEnter your choice: ")
            if choice == '1':
                self.create_group()
                self.pause_and_clear()
            elif choice == '2':
                self.add_expense()
                self.pause_and_clear()
            elif choice == '3':
                self.view_balances()
                self.pause_and_clear()
            elif choice == '4':
                self.settle_debts()
                self.pause_and_clear()
            elif choice == '5':
                self.record_payment()
                self.pause_and_clear()
            elif choice == '6':
                self.show_help()
                self.pause_and_clear()
            elif choice == '7':
                print("Goodbye!")
                sys.exit()
            else:
                print("Invalid choice. Please try again.")
                self.pause_and_clear()

    def create_group(self):
        group_name = input("Enter group name: ").strip()
        if not group_name:
            print("Group name cannot be empty.")
            return
        member_names = input("Enter member names separated by commas: ").split(',')
        member_names = [name.strip() for name in member_names if name.strip()]
        if not member_names:
            print("At least one member is required to create a group.")
            return
        success = self.data_manager.create_group(group_name, member_names)
        if success:
            print(f"Group '{group_name}' created with members: {', '.join(member_names)}")

    def add_expense(self):
        group_name = input("Enter group name: ").strip()
        group = self.data_manager.get_group(group_name)
        if not group:
            print(f"Group '{group_name}' not found.")
            return
        paid_by = input("Enter the name of the person who paid: ").strip()
        if paid_by not in group.members:
            print(f"{paid_by} is not a member of the group '{group_name}'.")
            return
        try:
            amount = float(input("Enter the amount: ").strip())
        except ValueError:
            print("Invalid amount.")
            return
        description = input("Enter a description: ").strip()
        involved_members_input = input("Enter involved members separated by commas (leave blank for all group members): ")
        if involved_members_input.strip():
            involved_members = [name.strip() for name in involved_members_input.split(',') if name.strip()]
            for member in involved_members:
                if member not in group.members:
                    print(f"{member} is not a member of the group '{group_name}'.")
                    return
        else:
            involved_members = group.members
        self.data_manager.add_expense(group_name, paid_by, amount, description, involved_members)
        print(f"Expense '{description}' added to group '{group_name}'.")

    def view_balances(self):
        group_name = input("Enter group name: ").strip()
        group = self.data_manager.get_group(group_name)
        if not group:
            print(f"Group '{group_name}' not found.")
            return
        balances = self.data_manager.calculate_balances(group_name)
        print(f"\nBalances for group '{group_name}':")
        for member, balance in balances.items():
            print(f"{member}: {balance:.2f} EUR")

    def settle_debts(self):
        group_name = input("Enter group name: ").strip()
        group = self.data_manager.get_group(group_name)
        if not group:
            print(f"Group '{group_name}' not found.")
            return
        balances = self.data_manager.calculate_balances(group_name)
        settlements = self.data_manager.settle_debts(balances)
        if settlements:
            print(f"\nSettlements for group '{group_name}':")
            for settlement in settlements:
                print(settlement)
        else:
            print("Everyone is settled up!")

    def record_payment(self):
        group_name = input("Enter group name: ").strip()
        group = self.data_manager.get_group(group_name)
        if not group:
            print(f"Group '{group_name}' not found.")
            return
        payer = input("Enter the name of the person who made the payment: ").strip()
        payee = input("Enter the name of the person who received the payment: ").strip()
        if payer not in group.members or payee not in group.members:
            print("Both payer and payee must be members of the group.")
            return
        try:
            amount = float(input("Enter the amount: ").strip())
        except ValueError:
            print("Invalid amount.")
            return
        if amount <= 0:
            print("Amount must be greater than zero.")
            return
        self.data_manager.record_payment(group_name, payer, payee, amount)
        print(f"Recorded payment of {amount:.2f} EUR from {payer} to {payee} in group '{group_name}'.")

    def show_help(self):
        print("\nHelp - Description of Each Function:")
        print("1. Create a Group:")
        print("   - Allows you to create a new group by specifying a group name and adding members.")
        print("2. Add Expense to Group:")
        print("   - Add a new expense to a group. You specify who paid, the amount, a description, and who was involved in the expense.")
        print("3. View Group Balances:")
        print("   - Displays the current balances for each member in the specified group.")
        print("   - Positive balance means the member is owed money.")
        print("   - Negative balance means the member owes money.")
        print("4. Settle Debts:")
        print("   - Calculates and displays the minimal set of transactions required to settle all debts within the group.")
        print("5. Record Payment:")
        print("   - Record a payment made from one member to another to settle debts.")
        print("   - This updates the balances to reflect the payment.")
        print("6. Help:")
        print("   - Displays this help message explaining what each function does.")
        print("7. Exit:")
        print("   - Exits the application.")
