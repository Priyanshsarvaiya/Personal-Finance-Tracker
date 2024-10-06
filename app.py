from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3

app = Flask(__name__)

# Database connection
def connect_db():
    conn = sqlite3.connect('finances.db')
    return conn

# Initialize the database with the transactions table
def init_db():
    conn = connect_db()
    with conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS transactions (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            type TEXT NOT NULL,
                            description TEXT NOT NULL,
                            amount REAL NOT NULL
                        )''')
    conn.close()

@app.route('/')
def index():
    conn = connect_db()
    cursor = conn.execute('SELECT * FROM transactions')
    transactions = cursor.fetchall()
    
    # Calculate total income, expense, and balance
    income = sum([transaction[3] for transaction in transactions if transaction[1] == 'Income'])
    expense = sum([transaction[3] for transaction in transactions if transaction[1] == 'Expense'])
    balance = income - expense

    conn.close()
    return render_template('index.html', transactions=transactions, income=income, expense=expense, balance=balance)

@app.route('/add', methods=['POST'])
def add_transaction():
    type = request.form['type']
    description = request.form['description']
    amount = float(request.form['amount'])

    conn = connect_db()
    conn.execute('INSERT INTO transactions (type, description, amount) VALUES (?, ?, ?)',
                 (type, description, amount))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_transaction(id):
    conn = connect_db()
    conn.execute('DELETE FROM transactions WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
