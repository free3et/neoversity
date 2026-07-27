def polynomial_hash(s, base=256, modulus=101): # polynomial_hash - обчислює поліноміальний хеш рядка
    n = len(s) # len(s) - довжина рядка
    hash_value = 0 # hash_value - значення хешу
    for i, char in enumerate(s):
        power_of_base = pow(base, n - i - 1) % modulus # обчислює степінь base в степені n - i - 1
        hash_value = (hash_value + ord(char) * power_of_base) % modulus # ord(char) - перетворює символ на його ASCII код   
    return hash_value # Повертаємо значення хешу

def rabin_karp_search(main_string, substring):
    # Довжини основного рядка та підрядка пошуку
    substring_length = len(substring)
    main_string_length = len(main_string)
    
    # Базове число для хешування та модуль
    base = 256 
    modulus = 101  
    
    # Хеш-значення для підрядка пошуку та поточного відрізка в основному рядку
    substring_hash = polynomial_hash(substring, base, modulus)
    current_slice_hash = polynomial_hash(main_string[:substring_length], base, modulus)
    
    # Попереднє значення для перерахунку хешу
    h_multiplier = pow(base, substring_length - 1) % modulus
    
    # Проходимо крізь основний рядок
    for i in range(main_string_length - substring_length + 1): # main_string_length - substring_length + 1 - довжина тексту - довжина підрядка + 1
        if substring_hash == current_slice_hash: # substring_hash - хеш підрядка, current_slice_hash - хеш поточного відрізка в основному рядку
            if main_string[i:i+substring_length] == substring: 
                return i # Повертаємо позицію підрядка в тексті

        if i < main_string_length - substring_length: # довжина тексту - довжина підрядка
            current_slice_hash = (current_slice_hash - ord(main_string[i]) * h_multiplier) % modulus # ord(main_string[i]) - перетворює символ на його ASCII код
            current_slice_hash = (current_slice_hash * base + ord(main_string[i + substring_length])) % modulus # ord(main_string[i + substring_length]) - перетворює символ на його ASCII код
            if current_slice_hash < 0: # хеш поточного відрізка в основному рядку
                current_slice_hash += modulus

    return -1