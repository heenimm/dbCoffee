import sqlite3

con = sqlite3.connect("coffee.sqlite")
cur = con.cursor()

cur.execute("""
CREATE TABLE coffee (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    roast TEXT,
    form TEXT,
    description TEXT,
    price REAL,
    volume TEXT
)
""")

cur.executemany("""
INSERT INTO coffee (name, roast, form, description, price, volume)
VALUES (?, ?, ?, ?, ?, ?)
""", [
    ("Арабика", "Светлая", "в зернах", "Фруктовый вкус", 250.0, "250г"),
    ("Робуста", "Темная", "молотый", "Горький и крепкий", 200.0, "500г"),
    ("Мокка", "Средняя", "в зернах", "Шоколадный оттенок", 300.0, "250г")
])

con.commit()
con.close()
