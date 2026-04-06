from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# Database
def init_db():
    conn = sqlite3.connect("database.db")
    
    conn.execute('''CREATE TABLE IF NOT EXISTS requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        service TEXT,
        details TEXT
    )''')

    # price column
    try:
        conn.execute("ALTER TABLE requests ADD COLUMN price INTEGER DEFAULT 0")
    except:
        pass

    # status column
    try:
        conn.execute("ALTER TABLE requests ADD COLUMN status TEXT DEFAULT 'Pending'")
    except:
        pass

    conn.close()

init_db()

# Home
@app.route('/')
def home():
    return render_template("form.html")

# Submit
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    email = request.form['email']
    service = request.form['service']
    details = request.form['details']

    conn = sqlite3.connect("database.db")
    conn.execute(
        "INSERT INTO requests (name, email, service, details) VALUES (?, ?, ?, ?)",
        (name, email, service, details)
    )
    conn.commit()
    conn.close()

    return "Request Submit ho gayi 👍"

# Admin
@app.route('/admin')
def admin():
    conn = sqlite3.connect("database.db")
    data = conn.execute("SELECT * FROM requests").fetchall()
    conn.close()
    return render_template("admin.html", data=data)

# Set price
@app.route('/set-price/<int:id>', methods=['POST'])
def set_price(id):
    price = request.form['price']

    conn = sqlite3.connect("database.db")
    conn.execute("UPDATE requests SET price=? WHERE id=?", (price, id))
    conn.commit()
    conn.close()

    return "Price updated 👍"

# Check bill
@app.route('/check', methods=['GET', 'POST'])
def check():
    if request.method == 'POST':
        email = request.form['email']

        conn = sqlite3.connect("database.db")
        data = conn.execute("SELECT * FROM requests WHERE email=?", (email,)).fetchall()
        conn.close()

        return render_template("check.html", data=data)

    return render_template("check.html")

# Payment
@app.route('/pay/<int:id>')
def pay(id):
    conn = sqlite3.connect("database.db")
    conn.execute("UPDATE requests SET status='Paid' WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return "Payment Successful ✅"

# Run
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
