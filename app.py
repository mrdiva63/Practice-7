import psycopg2
import csv
import sys


try:
    conn = psycopg2.connect(
        dbname="postgres", 
        user="postgres",
        password="password",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()
    print("Connected to database!")
except Exception as e:
    print(f"Connection error: {e}")
    sys.exit()


cur.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        phone VARCHAR(20) UNIQUE NOT NULL
    );
""")
conn.commit()

def add_contact(name, phone):
    try:
        cur.execute(
            "INSERT INTO contacts (name, phone) VALUES (%s, %s) "
            "ON CONFLICT (phone) DO UPDATE SET name = EXCLUDED.name", 
            (name, phone)
        )
        conn.commit()
        print(f"Contact {name} added/updated!")
    except Exception as e:
        print("Error adding contact:", e)
        conn.rollback()

def load_from_csv(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                add_contact(row['name'], row['phone'])
        print("CSV data loaded successfully!")
    except FileNotFoundError:
        print("CSV file not found.")

def get_contacts():
    cur.execute("SELECT id, name, phone FROM contacts ORDER BY name")
    for row in cur.fetchall():
        print(f"ID: {row[0]} | Name: {row[1]} | Phone: {row[2]}")

def update_contact(name, new_phone):
    cur.execute("UPDATE contacts SET phone=%s WHERE name=%s", (new_phone, name))
    conn.commit()
    print("Contact updated!")

def delete_contact(name_or_phone):
 
    cur.execute("DELETE FROM contacts WHERE name=%s OR phone=%s", (name_or_phone, name_or_phone))
    conn.commit()
    print("Contact deleted!")

def search_contacts(query):
   
    cur.execute(
        "SELECT * FROM contacts WHERE name ILIKE %s OR phone LIKE %s",
        ('%' + query + '%', query + '%')
    )
    results = cur.fetchall()
    for r in results:
        print(r)


while True:
    print("\n--- PhoneBook (Practice 7) ---")
    print("1.Add  2.Show All  3.Search  4.Update  5.Delete  6.Upload CSV  7.Exit")
    choice = input("Choose action: ")

    if choice == "1":
        add_contact(input("Name: "), input("Phone: "))
    elif choice == "2":
        get_contacts()
    elif choice == "3":
        search_contacts(input("Enter name or phone prefix: "))
    elif choice == "4":
        update_contact(input("Name to update: "), input("New phone: "))
    elif choice == "5":
        delete_contact(input("Enter name or phone to delete: "))
    elif choice == "6":
        load_from_csv('contacts.csv')
    elif choice == "7":
        break

cur.close()
conn.close()