import csv
import os

# List to store all contacts
contacts = []
FILE_NAME = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "contacts.csv"
)

# Load contacts from CSV file when the program starts
def load_contacts():
    if not os.path.exists(FILE_NAME):
        return

    try:
        with open(FILE_NAME, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row.get("name") and row.get("phone"):
                    contacts.append({
                        "name": row["name"],
                        "phone": row["phone"],
                        "email": row.get("email", "")
                    })
    except (OSError, csv.Error) as error:
        print("Could not load contacts:", error)


# Save all contacts to CSV file
def save_contacts():
    try:
        with open(FILE_NAME, "w", newline="", encoding="utf-8") as file:
            fieldnames = ["name", "phone", "email"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(contacts)
    except OSError as error:
        print("Could not save contacts:", error)


# Validate a 10-digit phone number
def valid_phone(phone):
    return len(phone) == 10 and phone.isdigit()


# 1. Create / Add Contact
def add_contact():
    name = input("Enter Name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return

    phone = input("Enter Phone (10 digits): ").strip()

    if not valid_phone(phone):
        print("Invalid phone number. Enter exactly 10 digits.")
        return

    for contact in contacts:
        if contact["phone"] == phone:
            print("Contact with this number already exists.")
            return

    email = input("Enter Email: ").strip()
    new_contact = {"name": name, "phone": phone, "email": email}
    contacts.append(new_contact)
    save_contacts()
    print(f"Contact added: {name} | {phone}")


# 2. Read / View All Contacts
def view_contacts():
    if len(contacts) == 0:
        print("No contacts saved yet.")
        return

    print("\n--- All Contacts ---")
    for contact in contacts:
        print(
            f"{contact['name']} | {contact['phone']} | "
            f"{contact['email']}"
        )


# 3. Search Contact by Name
def search_contact():
    query = input("Enter Name to search: ").strip().lower()
    if not query:
        print("Please enter a name to search.")
        return

    found = False
    for contact in contacts:
        if query in contact["name"].lower():
            print(
                f"{contact['name']} | {contact['phone']} | "
                f"{contact['email']}"
            )
            found = True

    if not found:
        print("Contact not found.")


# 4. Update Contact Phone Number
def update_contact():
    name = input("Enter Name to update: ").strip().lower()

    for contact in contacts:
        if contact["name"].lower() == name:
            new_phone = input("Enter new phone number: ").strip()

            if not valid_phone(new_phone):
                print("Invalid phone number. Enter exactly 10 digits.")
                return

            for other in contacts:
                if other["phone"] == new_phone and other is not contact:
                    print("Contact with this number already exists.")
                    return

            contact["phone"] = new_phone
            save_contacts()
            print(f"Phone updated: {new_phone}")
            return

    print("Contact not found.")


# 5. Delete Contact
def delete_contact():
    name = input("Enter Name to delete: ").strip().lower()

    for contact in contacts:
        if contact["name"].lower() == name:
            contacts.remove(contact)
            save_contacts()
            print(
                f"Contact '{contact['name']}' deleted. "
                f"Total contacts: {len(contacts)}"
            )
            return

    print("Contact not found.")


# Main Menu Loop
def main():
    load_contacts()

    while True:
        print("\n--- Contact Management System ---")
        print("1. Add Contact")
        print("2. View Contacts")
        print("3. Search Contact")
        print("4. Update Contact")
        print("5. Delete Contact")
        print("6. Exit")

        choice = input("Choose an option (1-6): ").strip()

        if choice == "1":
            add_contact()
        elif choice == "2":
            view_contacts()
        elif choice == "3":
            search_contact()
        elif choice == "4":
            update_contact()
        elif choice == "5":
            delete_contact()
        elif choice == "6":
            save_contacts()
            print("Exiting program...")
            break
        else:
            print("Invalid option! Please enter 1 to 6.")


if __name__ == "__main__":
    main()
