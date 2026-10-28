import sqlite3
import os
from datetime import datetime
 
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Stock_Data.db')
 
MENU = ("\n1. Enter Date for Stock Data\n"
        "2. Add Stock Data\n"
        "3. Exit\n"
        "4. View Available Dates\n"
        "5. Update Data\n"
        "Enter your choice (1-4): ")
 
MENU1 = ("\n1. Update Open price\n"
         "2. Update High price\n"
         "3. Update Low price\n"
         "4. Update Close price\n"
         "5. Update volume\n"
         "6.Update all data\n"
         "Enter your choice (1-6): ")


CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS stock_prices (
    date TEXT PRIMARY KEY,
    exchange TEXT NOT NULL,
    symbol TEXT NOT NULL,
    open REAL,
    high REAL,
    low REAL,
    close REAL,
    volume INTEGER
)
"""
 
SEED_DATA = [
    ('2026-10-01', 'NSE', 'RELIANCE', 1180.1, 1183.9, 1160.8, 1167.7, 16771221),
    ('2026-10-05', 'NSE', 'RELIANCE', 1171.2, 1193.0, 1171.2, 1186.4, 14254907),
    ('2026-10-06', 'NSE', 'RELIANCE', 1188.1, 1219.1, 1188.1, 1218.0, 18003127),
    ('2026-10-07', 'NSE', 'RELIANCE', 1212.0, 1220.8, 1203.5, 1207.7, 11880731),
    ('2026-10-08', 'NSE', 'RELIANCE', 1207.7, 1208.0, 1173.0, 1178.0, 13965493),
    ('2026-10-09', 'NSE', 'RELIANCE', 1179.0, 1179.0, 1160.2, 1170.3, 12086708),
    ('2026-10-12', 'NSE', 'RELIANCE', 1180.3, 1185.5, 1153.2, 1158.9, 11338332),
    ('2026-10-13', 'NSE', 'RELIANCE', 1158.9, 1168.3, 1152.2, 1166.7, 10988483),
    ('2026-10-14', 'NSE', 'RELIANCE', 1167.0, 1188.0, 1162.7, 1174.6, 10938195),
    ('2026-10-15', 'NSE', 'RELIANCE', 1185.2, 1218.8, 1177.2, 1215.0, 23456219),
    ('2026-10-16', 'NSE', 'RELIANCE', 1215.0, 1215.4, 1193.0, 1211.2, 17225283),
    ('2026-10-19', 'NSE', 'RELIANCE', 1212.0, 1228.2, 1201.0, 1202.0, 15572554),
    ('2026-10-21', 'NSE', 'RELIANCE', 1212.0, 1234.3, 1199.3, 1209.0, 17607823),
    ('2026-10-22', 'NSE', 'RELIANCE', 1206.2, 1208.0, 1184.5, 1184.5, 14957042),
    ('2026-10-23', 'NSE', 'RELIANCE', 1184.0, 1201.9, 1163.1, 1190.0, 14905641),
]
 
 
def setup_database():
    """Create the table if needed and fill it with the starting data if it is empty."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute(CREATE_TABLE)
    count = conn.execute("SELECT COUNT(*) FROM stock_prices").fetchone()[0]
    if count == 0:
        conn.executemany(
            """INSERT INTO stock_prices
               (date, exchange, symbol, open, high, low, close, volume)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            SEED_DATA)
        conn.commit()
        print("New database created with starting data.")
    return conn
 
 
def is_valid_date(date):
    try:
        datetime.strptime(date, '%Y-%m-%d')
        return True
    except ValueError:
        return False
 
 
def date_exists(conn, date):
    return conn.execute(
        "SELECT date FROM stock_prices WHERE date = ?", (date,)
    ).fetchone() is not None
 
 
def view_available_dates(conn):
    print("Available dates in the database:")
    rows = conn.execute("SELECT date FROM stock_prices ORDER BY date").fetchall()
    for row in rows:
        print(row[0])
 
 
def view_stock_data(conn):
    date = input("Enter the date (YYYY-MM-DD): ").strip()
 
    if not is_valid_date(date):
        print("Invalid format. Please use YYYY-MM-DD.")
        return
 
    first_date, last_date = conn.execute(
        "SELECT MIN(date), MAX(date) FROM stock_prices"
    ).fetchone()
    if date < first_date or date > last_date:
        print(f"Date out of range. Please enter a date between {first_date} and {last_date}.")
        return
 
    row = conn.execute(
        "SELECT date, open, high, low, close, volume FROM stock_prices WHERE date = ?",
        (date,),
    ).fetchone()
    if row is None:
        print(f"No data available for {date}.")
        return
 
    print(f"Stock data for {date}:")
    print("Date   =", row[0])
    print("Open   =", row[1])
    print("High   =", row[2])
    print("Low    =", row[3])
    print("Close  =", row[4])
    print("Volume =", row[5])
 
def update_stock_data(conn):
    date = input("Enter the date (YYYY-MM-DD): ")

    if not is_valid_date(date):
        print("Invalid format. Please use YYYY-MM-DD.")
        return

    if date_exists(conn, date):
        print(f"For date: {date}\n"
              f"{MENU1}")
        
        return
    
    try:
       while True:
           choice1 = input(MENU1).strip() 

           if choice1 == '1':
               open1 = int(input("Enter new open value: "))
               conn.execute("UPDATE stock_prices SET open = ? WHERE date = ?", (open1, date))
    except:
        print("Prices must be numbers and volume must be a whole number.")           
               
               

    

def add_stock_data(conn):
    date = input("Enter the date (YYYY-MM-DD): ").strip()
 
    if not is_valid_date(date):
        print("Invalid format. Please use YYYY-MM-DD.")
        return
 
    if not date_exists(conn, date):
        print("Date doesn't exist")
        return

    print(f"Updating data for {date}")
 
    try:
        open_price = float(input("Enter the opening price: ").strip())
        high_price = float(input("Enter the highest price: ").strip())
        low_price = float(input("Enter the lowest price: ").strip())
        close_price = float(input("Enter the closing price: ").strip())
        volume = int(input("Enter the volume: ").strip())
    except ValueError:
        print("Prices must be numbers and volume must be a whole number.")
        return
 
    exchange, symbol = conn.execute(
        "SELECT exchange, symbol FROM stock_prices LIMIT 1"
    ).fetchone()
 
    conn.execute(
        """INSERT INTO stock_prices (date, exchange, symbol, open, high, low, close, volume)
           VALUES (:date, :exchange, :symbol, :open, :high, :low, :close, :volume)""",
        {
            'date': date,
            'exchange': exchange,
            'symbol': symbol,
            'open': open_price,
            'high': high_price,
            'low': low_price,
            'close': close_price,
            'volume': volume
        })
    conn.commit()
    print(f"Data for {date} added.")
 
 
conn = setup_database()
 
while True:
    choice = input(MENU).strip()
 
    if choice == '1':
        view_stock_data(conn)
    elif choice == '2':
        add_stock_data(conn)
    elif choice == '3':
        break
    elif choice == '4':
        view_available_dates(conn)
    elif choice == '5':
        update_stock_data(conn)
    else:
        print("Invalid choice. Please enter 1-4.")
 
conn.close()