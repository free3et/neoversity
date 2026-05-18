from collections import UserDict
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

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

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