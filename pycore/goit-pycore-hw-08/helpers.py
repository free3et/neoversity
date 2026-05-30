from classes import Record, Phone, Birthday
from classes import AddressBook
import pickle

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e) if str(e) else "Invalid value ❌"
        except KeyError:
            return "Contact not found 🚫"
        except IndexError:
            return "Not enough arguments for the command ⚠️"
        except TypeError:
            return "Invalid argument ❌"
    return inner


def parse_input(user_input):
    if not user_input.strip():
        return "", []

    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args, book):
    if len(args) < 2:
        raise ValueError("Use: add [name] [phone]")
    name, phone, *_ = args
    Phone(phone)

    record = book.find(name)
    message = "Contact updated 🔁!"

    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added 🎉!"
    if phone:
        record.add_phone(phone)
    return message


@input_error
def change_contact(args, book):
    if len(args) < 3:
        raise ValueError("Use: change [name] [old phone] [new phone]")
    name, old_phone, new_phone = args[:3]
    Phone(new_phone)

    record = book.find(name)
    if not record:
        raise KeyError

    record.edit_phone(old_phone, new_phone)
    return "Contact updated 🔁!"


@input_error
def show_phone(args, book):
    if len(args) < 1:
        raise ValueError("Use: phone [name]")
    name = args[0]
    record = book.find(name)
    if not record:
        raise KeyError

    return "; ".join(p.value for p in record.phones)


@input_error
def show_all(book):
    if not book.data:
        return "No contacts found."

    result = ""
    for name, record in book.data.items():
        result += f"🙋‍♀️{name}: 📱{'; '.join(p.value for p in record.phones)}\n"
    return result.strip()


@input_error
def add_birthday(args, book):
    if len(args) < 2:
        raise ValueError("Use: add-birthday [name] [DD.MM.YYYY]")
    name, date = args[:2]
    birthday = Birthday(date)

    record = book.find(name)
    if not record:
        raise KeyError
    record.birthday = birthday
    return "Birthday added 🎉!"


@input_error
def show_birthday(args, book):
    if len(args) < 1:
        raise ValueError("Use: show-birthday [name]")
    name = args[0]
    record = book.find(name)
    if not record:
        raise KeyError
    if not record.birthday:
        raise ValueError("Birthday is not set for this contact")

    return record.birthday.value.strftime("%d.%m.%Y")


@input_error
def birthdays(args, book):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No birthdays this week."
    return "\n".join(f"{item['name']}: {item['congratulation_date']}" for item in upcoming)
