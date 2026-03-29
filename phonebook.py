import csv
from connect import get_connection

def init_db():
    """Создает таблицу при первом запуске"""
    conn = get_connection()
    if conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                phone VARCHAR(20) UNIQUE NOT NULL
            );
        """)
        conn.commit()
        cur.close()
        conn.close()

def add_contact(name, phone):
    conn = get_connection()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO contacts (name, phone) VALUES (%s, %s) "
                "ON CONFLICT (phone) DO UPDATE SET name = EXCLUDED.name", 
                (name, phone)
            )
            conn.commit()
            print(f"Contact {name} added/updated!")
        except Exception as e:
            print("Error:", e)
            conn.rollback()
        finally:
            cur.close()
            conn.close()

def get_contacts():
    conn = get_connection()
    if conn:
        cur = conn.cursor()
        cur.execute("SELECT name, phone FROM contacts ORDER BY name")
        for row in cur.fetchall():
            print(f"{row[0]}: {row[1]}")
        cur.close()
        conn.close()

def search_contacts(query):
    conn = get_connection()
    if conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM contacts WHERE name ILIKE %s OR phone LIKE %s",
            ('%' + query + '%', query + '%')
        )
        for r in cur.fetchall():
            print(r)
        cur.close()
        conn.close()

def update_phone(name, new_phone):
    conn = get_connection()
    if conn:
        cur = conn.cursor()
        cur.execute("UPDATE contacts SET phone=%s WHERE name=%s", (new_phone, name))
        conn.commit()
        cur.close()
        conn.close()
        print("Updated!")

def delete_contact(identifier):
    conn = get_connection()
    if conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM contacts WHERE name=%s OR phone=%s", (identifier, identifier))
        conn.commit()
        cur.close()
        conn.close()
        print("Deleted!")

def load_from_csv(file):
    try:
        with open(file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                add_contact(row['name'], row['phone'])
    except FileNotFoundError:
        print("File not found!")

if __name__ == "__main__":
    init_db()
    while True:
        print("\n1.Add 2.Show 3.Search 4.Update 5.Delete 6.CSV 7.Exit")
        choice = input("Choose: ")
        if choice == "1":
            add_contact(input("Name: "), input("Phone: "))
        elif choice == "2":
            get_contacts()
        elif choice == "3":
            search_contacts(input("Query: "))
        elif choice == "4":
            update_phone(input("Name: "), input("New phone: "))
        elif choice == "5":
            delete_contact(input("Name/Phone: "))
        elif choice == "6":
            load_from_csv('contacts.csv')
        elif choice == "7":
            break