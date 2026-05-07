def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def add_contact(args, contacts):

    if len(args) != 2:
        return "Invalid command."
    name, phone = args
    contacts[name] = phone
    return "Contact added ✅."

def change_contact(args, contacts):

    if len(args) != 2:
        return "Invalid command ❌."

    name, phone = args
    if name in contacts:
        contacts[name] = phone
        return "Contact updated 🔁."
    return "Contact not found ❌."

def show_phone(args, contacts):

    if len(args) != 1:
        return "Invalid command ❌."
    name = args[0]
    if name in contacts:
        return contacts[name]
    return "Contact not found ❌."

def show_all(contacts):

    if not contacts:
        return "No contacts found ❌."

    result = ""
    for name, phone in contacts.items():
        result += f"🙋‍♀️{name}: 📱{phone}\n"
    return result.strip()