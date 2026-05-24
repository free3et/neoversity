from collections import UserDict
import datetime
import re 

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Name cannot be empty!")
        super().__init__(value)

class Phone(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Phone cannot be empty")
        if not re.match(r'^\d{10}$', value):
            raise ValueError("Phone must be 10 digits long!")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Birthday cannot be empty")
        if not re.match(r'^\d{2}\.\d{2}\.\d{4}$', value):
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        try:
            normalized_date = datetime.datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date. Check day and month values.")
        super().__init__(normalized_date)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone: str):
        self.phones.append(Phone(phone))
        return "Phone added successfully"

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p

        return None

    def edit_phone(self,old_phone: str, new_phone: str):
        phone = self.find_phone(old_phone)

        if phone:
            self.phones.remove(phone)
            self.phones.append(Phone(new_phone))
            return "Phone changed successfully!"
        else:
            raise ValueError(f"Phone {old_phone} not found")

    def remove_phone(self, phone: str):
        phone = self.find_phone(phone)

        if phone:
            self.phones.remove(phone)
            return "Phone deleted successfully"
        return "Phone not found"

    def add_birthday(self, birthday: str):
        self.birthday = Birthday(birthday)
        return "Birthday added successfully"

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: str):
        return self.data.get(name)

    def delete(self, name: str):
        if name not in self.data:
            raise ValueError(f"Record {name} not found")
        del self.data[name]
        return "Record deleted successfully!"

    def get_upcoming_birthdays(self):
        upcoming_birthdays = []
        today_day = datetime.datetime.today().date()

        for record in self.data.values():
            if not record.birthday:
                continue

            user_birthday = record.birthday.value.date()
            birthday_this_year = user_birthday.replace(year=today_day.year)

            if birthday_this_year < today_day:
                birthday_this_year = birthday_this_year.replace(year=today_day.year + 1)

            delta_days = (birthday_this_year - today_day).days

            if 0 <= delta_days <= 7:
                congratulation_date = birthday_this_year
                if congratulation_date.weekday() == 5:
                    congratulation_date = congratulation_date + datetime.timedelta(days=2)
                elif congratulation_date.weekday() == 6:
                    congratulation_date = congratulation_date + datetime.timedelta(days=1)

                upcoming_birthdays.append({
                    'name': record.name.value,
                    'congratulation_date': congratulation_date.strftime('%Y.%m.%d'),
                })
        return upcoming_birthdays