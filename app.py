import psycopg2
import csv

conn = psycopg2.connect(
    dbname="phonebook",
    user="postgres",
    password="1234",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

print("Connected to database!")



def add_contact(name, phone):
    try:
        cur.execute(
            "INSERT INTO contacts (name, phone) VALUES (%s, %s)",
            (name, phone)
        )
        conn.commit()
        print("Contact added!")
    except Exception as e:
        print("Error:", e)
        conn.rollback()


def get_contacts():
    cur.execute("SELECT * FROM contacts")
    rows = cur.fetchall()
    for row in rows:
        print(row)

def update_phone(name, new_phone):
    cur.execute(
        "UPDATE contacts SET phone=%s WHERE name=%s",
        (new_phone, name)
    )
    conn.commit()

def delete_contact(name):
    cur.execute(
        "DELETE FROM contacts WHERE name=%s",
        (name,)
    )
    conn.commit()

def search_by_name(name):
    cur.execute(
        "SELECT * FROM contacts WHERE name ILIKE %s",
        ('%' + name + '%',)
        
    )
    print(cur.fetchall())

def search_by_prefix(prefix):
    cur.execute(
        "SELECT * FROM contacts WHERE phone LIKE %s",
        (prefix + '%',)
    )
    print(cur.fetchall())



def load_from_csv(file):
    with open(file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            add_contact(row['name'], row['phone'])

            

while True:
    print("\n1.Add 2.Show 3.Search 4.Update 5.Delete 6.Exit")
    choice = input("Choose: ")

    if choice == "1":
        name = input("Name: ")
        phone = input("Phone: ")
        add_contact(name, phone)

    elif choice == "2":
        get_contacts()

    elif choice == "3":
        name = input("Search name: ")
        search_by_name(name)

    elif choice == "4":
        name = input("Name: ")
        phone = input("New phone: ")
        update_phone(name, phone)

    elif choice == "5":
        name = input("Delete name: ")
        delete_contact(name)

    elif choice == "6":
        break

cur.close()
conn.close()