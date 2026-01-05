import sqlite3

sq = sqlite3.connect("database.db")
cursor = sq.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS admin (
    username TEXT,
    password TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS accounts (
    name TEXT,
    card_number TEXT,
    cvv2 TEXT,
    expire_date TEXT,
    balance INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS enteghal (
    from_card TEXT,
    to_card TEXT,
    amount INTEGER
)
""")

cursor.execute("""
INSERT INTO admin VALUES ('admin', '1234')
""")

cursor.execute("""
INSERT INTO accounts VALUES
('nikan', '6037991111111111', '123', '06/27', 5000000),
('arad', '6037992222222222', '456', '09/26', 3000000)
""")

sq.commit()
sq.close()