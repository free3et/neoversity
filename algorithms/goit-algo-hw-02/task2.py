from collections import deque

'''
Необхідно розробити функцію, яка приймає рядок як вхідний параметр, додає всі його символи до двосторонньої черги (deque з модуля collections в Python), а потім порівнює символи з обох кінців черги, щоб визначити, чи є рядок паліндромом.
'''

def check_palindrome(str_input):
    deque_string = deque(str_input.lower().replace(' ', '')) # приводимо рядок до нижнього регістру і прибираємо пробіли
    result_right = ''
    result_left = ''
    is_palindrome = True

    while len(deque_string) > 1:
        result_left += deque_string.popleft() # додаємо символ зліва в результат
        result_right += deque_string.pop() # додаємо символ справа в результат
        if result_left != result_right: # якщо символи зліва і справа не рівні, то рядок не є паліндромом
            is_palindrome = False
            break # якщо рядок не є паліндромом, то виходимо з циклу
    return is_palindrome

print(check_palindrome('Madam')) # True
print(check_palindrome('hello')) # False
print(check_palindrome('Step on no pets')) # True
print(check_palindrome('No lemon no melon')) # True