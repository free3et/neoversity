def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Enter the argument for the command"

        except KeyError:
            return "Contact not found."

        except IndexError:
            return "Enter the argument for the command"

        except TypeError:
            return "Invalid argument."
    return inner

def parse_input(user_input):
    if not user_input.strip():
        return "", []

    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, contacts):
    name, phone = args
    contacts[name] = phone
    return "Contact added ✅."

@input_error
def change_contact(args, contacts):
    name, phone = args
    if name not in contacts:
        raise KeyError

    contacts[name] = phone
    return "Contact updated 🔁."

@input_error
def show_phone(args, contacts):
    name = args[0]
    if name not in contacts:
        raise KeyError

    return contacts[name]

@input_error
def show_all(contacts):
    if not contacts:
        return "No contacts found."
        
    result = ""
    for name, phone in contacts.items():
        result += f"🙋‍♀️{name}: 📱{phone}\n"
    return result.strip()