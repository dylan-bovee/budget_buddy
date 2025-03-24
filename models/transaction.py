class Transaction:
    def __init__(self, transaction_type, amount, description, date):
        self.transaction_type = transaction_type
        self.amount = amount
        self.description = description
        self.date = date
