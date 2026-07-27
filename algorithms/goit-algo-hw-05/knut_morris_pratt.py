def compute_lps(pattern): # compute_lps - обчислює довжину найбільшого префікса, який є суфіксом
    lps = [0] * len(pattern) 
    length = 0
    i = 1

    while i < len(pattern): # len(pattern) - довжина підрядка
        if pattern[i] == pattern[length]: # pattern[i] - символ підрядка, pattern[length] - символ префікса
            length += 1 # length - довжина префікса
            lps[i] = length # lps[i] - довжина найбільшого префікса, який є суфіксом
            i += 1
        else:
            if length != 0: # length - довжина префікса
                length = lps[length - 1] # lps[length - 1] - довжина найбільшого префікса, який є суфіксом
            else:
                lps[i] = 0 # lps[i] - довжина найбільшого префікса, який є суфіксом
                i += 1

    return lps

def kmp_search(main_string, pattern): # kmp_search - пошуковий алгоритм Кнута-Морріса-Пратта
    M = len(pattern) # len(pattern) - довжина підрядка
    N = len(main_string) # len(main_string) - довжина тексту

    lps = compute_lps(pattern) # lps - довжина найбільшого префікса, який є суфіксом

    i = j = 0 # i - індекс тексту, j - індекс підрядка

    while i < N:
        if pattern[j] == main_string[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1] # lps[j - 1] - довжина найбільшого префікса, який є суфіксом
        else:
            i += 1 # i - індекс тексту

        if j == M:
            return i - j # Повертаємо позицію підрядка в тексті

    return -1  # якщо підрядок не знайдено
