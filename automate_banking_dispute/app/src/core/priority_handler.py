import sqlite3

class TransactionPriority:
    def __init__(self, db_name=r"C:\Users\dashu\Desktop\personal_projects\automate_banking_dispute\app\database\sql_db\transactions.db"):
        """
        Initializes the TransactionPriority class with a database connection.
        :param db_name: Path to the SQLite database file.
        """
        self.db_name = db_name

    def _connect_db(self):
        """
        Establishes a connection to the SQLite database.
        :return: SQLite connection object.
        """
        return sqlite3.connect(self.db_name)

    def get_transaction_count(self, user_id):
        """
        Retrieves the number of transactions associated with a user ID.
        :param user_id: The ID of the user.
        :return: Integer count of transactions.
        """
        try:
            with self._connect_db() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM transactions WHERE user_id = ?", (user_id,))
                count = cursor.fetchone()[0] or 0  # Ensure count is not None
                return count
        except sqlite3.DatabaseError as e:
            print(f"Database error: {e}")
            return 0  # Return default count in case of an error

    def calculate_priority(self, transaction_count):
        """
        Normalizes transaction count to a priority score between 0 and 1.
        :param transaction_count: The number of transactions.
        :return: Normalized priority score.
        """
        max_transactions = 20  # Define a threshold for max transactions
        return min(1.0, transaction_count / max_transactions)  # Normalize between 0 and 1

    def get_priority(self, user_id):
        """
        Retrieves the priority score for a given user based on transaction history.
        :param user_id: The ID of the user.
        :return: Priority score (0 to 1).
        """
        transaction_count = self.get_transaction_count(user_id)

        if transaction_count == 0:
            print(f"No transactions found for User ID {user_id}. Assigning priority 0.")
            return 0.0  # Explicitly return a float for consistency

        return self.calculate_priority(transaction_count)

# Example usage
# if __name__ == "__main__":
#     tp = TransactionPriority()
#     user_id = int(input("Enter User ID: "))
#     priority = tp.get_priority(user_id)
#     print(f"Priority Score for User ID {user_id}: {priority:.2f}")
