class BloomFilter:
    def __init__(self, size, num_hashes):
        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = [0] * size

    def add(self, password):
        for i in range(self.num_hashes):
            index = hash(f"{password}{i}") % self.size
            self.bit_array[index] = 1

    def contains(self, password):
        for i in range(self.num_hashes):
            index = hash(f"{password}{i}") % self.size
            if self.bit_array[index] == 0:
                return False
        return True

def check_password_uniqueness(bloom: BloomFilter, passwords: list[str]) -> list[str]:
    results = []
    for password in passwords:
        if not isinstance(password, str) or password == "":
            results.append("некоректний пароль")
            continue
        results.append("уже використаний" if bloom.contains(password) else "унікальний")

    return results

if __name__ == "__main__":
    # Ініціалізація фільтра Блума
    bloom = BloomFilter(size=1000, num_hashes=3)

    # Додавання існуючих паролів
    existing_passwords = ["password123", "admin123", "qwerty123", "", None]
    for password in existing_passwords:
        bloom.add(password)

    # Перевірка нових паролів
    new_passwords_to_check = ["password123", "newpassword", "admin123", "guest"]
    results = check_password_uniqueness(bloom, new_passwords_to_check)

    # Виведення результатів
    for password, status in zip(new_passwords_to_check, results):
        print(f"Пароль '{password}' - {status}.")
