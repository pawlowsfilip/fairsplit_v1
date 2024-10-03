import json
import os
import uuid
from datetime import datetime
import heapq
from models import Group

DATA_DIR = 'data'

class DataManager:
    def __init__(self):
        self.groups_file = os.path.join(DATA_DIR, 'groups.json')
        self._ensure_data_dir()
        self.groups = self._load_data(self.groups_file)

    def _ensure_data_dir(self):
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)

    def _load_data(self, file_path):
        if not os.path.exists(file_path):
            return {}
        with open(file_path, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}

    def _save_data(self, file_path, data):
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)

    def create_group(self, group_name, members):
        if group_name in self.groups:
            print(f"Group '{group_name}' already exists.")
            return False
        group_id = str(uuid.uuid4())
        group = {
            'id': group_id,
            'name': group_name,
            'members': members,
            'expenses': []
        }
        self.groups[group_name] = group
        self._save_data(self.groups_file, self.groups)
        return True

    def get_group(self, group_name):
        group_data = self.groups.get(group_name)
        if group_data:
            return Group(**group_data)
        else:
            return None

    def add_expense(self, group_name, paid_by, amount, description, involved_members):
        group = self.groups[group_name]
        expense_id = str(uuid.uuid4())
        expense = {
            'id': expense_id,
            'group_id': group['id'],
            'description': description,
            'amount': amount,
            'paid_by': paid_by,
            'date': str(datetime.now()),
            'involved_members': involved_members,
            'splits': {},
            'type': 'expense'
        }
        split_amount = amount / len(involved_members)
        for member in involved_members:
            expense['splits'][member] = split_amount
        group['expenses'].append(expense)
        self.groups[group_name] = group
        self._save_data(self.groups_file, self.groups)

    def record_payment(self, group_name, payer, payee, amount):
        group = self.groups[group_name]
        payment = {
            'id': str(uuid.uuid4()),
            'group_id': group['id'],
            'amount': amount,
            'payer': payer,
            'payee': payee,
            'date': str(datetime.now()),
            'type': 'payment'
        }
        group['expenses'].append(payment)
        self.groups[group_name] = group
        self._save_data(self.groups_file, self.groups)

    def calculate_balances(self, group_name):
        group = self.groups[group_name]
        balances = {member: 0 for member in group['members']}
        for expense in group['expenses']:
            if expense.get('type') == 'payment':
                # Handle payments
                payer = expense['payer']
                payee = expense['payee']
                amount = expense['amount']
                balances[payer] += amount
                balances[payee] -= amount
            else:
                # Handle expenses
                amount = expense['amount']
                paid_by = expense['paid_by']
                splits = expense['splits']
                for member, split_amount in splits.items():
                    if member == paid_by:
                        balances[member] += (amount - split_amount)
                    else:
                        balances[member] -= split_amount
        return balances

    def settle_debts(self, balances):
        settlements = []
        creditors = []
        debtors = []
        for person, balance in balances.items():
            if balance > 0.01:
                heapq.heappush(creditors, (-balance, person))
            elif balance < -0.01:
                heapq.heappush(debtors, (balance, person))
        while creditors and debtors:
            credit_amount, creditor = heapq.heappop(creditors)
            debt_amount, debtor = heapq.heappop(debtors)
            settle_amount = min(-debt_amount, -credit_amount)
            settlements.append(f"{debtor} owes {creditor}: {settle_amount:.2f} EUR")
            remaining_credit = credit_amount + settle_amount
            remaining_debt = debt_amount + settle_amount
            if remaining_credit < -0.01:
                heapq.heappush(creditors, (remaining_credit, creditor))
            if remaining_debt > 0.01:
                heapq.heappush(debtors, (remaining_debt, debtor))
        return settlements
