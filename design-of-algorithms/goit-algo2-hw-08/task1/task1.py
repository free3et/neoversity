import random
from typing import Dict
import time
from collections import deque


class SlidingWindowRateLimiter:
    def __init__(self, window_size: int = 10, max_requests: int = 1):
        self.window_size = window_size
        self.max_requests = max_requests
        # user_id -> deque з часовими мітками повідомлень у поточному вікні
        self.user_windows: Dict[str, deque] = {}

    def _cleanup_window(self, user_id: str, current_time: float) -> None:
        #Видаляє застарілі мітки з вікна користувача. Якщо вікно стало порожнім — видаляє запис про користувача
        window = self.user_windows.get(user_id)
        if window is None:
            return

        # Видаляємо всі мітки, старші за window_size секунд
        while window and current_time - window[0] >= self.window_size:
            window.popleft()

        # Якщо у вікні не залишилось повідомлень — видаляємо користувача
        if not window:
            del self.user_windows[user_id]

    def can_send_message(self, user_id: str) -> bool:
        # Перевіряє, чи може користувач надіслати повідомлення зараз
        current_time = time.time()
        self._cleanup_window(user_id, current_time)

        window = self.user_windows.get(user_id)
        # Перше повідомлення (або вікно очищене) — завжди дозволено
        if window is None:
            return True
        return len(window) < self.max_requests

    def record_message(self, user_id: str) -> bool:
        # Записує повідомлення, якщо ліміт не перевищено. Повертає True, якщо повідомлення прийнято, інакше False
        if not self.can_send_message(user_id):
            return False

        current_time = time.time()
        if user_id not in self.user_windows:
            self.user_windows[user_id] = deque()
        self.user_windows[user_id].append(current_time)
        return True

    def time_until_next_allowed(self, user_id: str) -> float:
        # Повертає час очікування (у секундах) до можливості надіслати наступне повідомлення. 0.0 — якщо можна вже зараз
        current_time = time.time()
        self._cleanup_window(user_id, current_time)

        window = self.user_windows.get(user_id)
        if window is None or len(window) < self.max_requests:
            return 0.0

        # Наступне повідомлення стане можливим, коли найстаріша мітка вийде за межі вікна
        wait = window[0] + self.window_size - current_time
        return max(0.0, wait)


# Демонстрація роботи
def test_rate_limiter():
    # Створюємо rate limiter: вікно 10 секунд, 1 повідомлення
    limiter = SlidingWindowRateLimiter(window_size=10, max_requests=1)

    # Симулюємо потік повідомлень від користувачів (послідовні ID від 1 до 20)
    print("\n=== Симуляція потоку повідомлень ===")
    for message_id in range(1, 11):
        # Симулюємо різних користувачів (ID від 1 до 5)
        user_id = message_id % 5 + 1

        result = limiter.record_message(str(user_id))
        wait_time = limiter.time_until_next_allowed(str(user_id))

        print(f"Повідомлення {message_id:2d} | Користувач {user_id} | "
              f"{'✓' if result else f'× (очікування {wait_time:.1f}с)'}")

        # Невелика затримка між повідомленнями для реалістичності
        # Випадкова затримка від 0.1 до 1 секунди
        time.sleep(random.uniform(0.1, 1.0))

    # Чекаємо, поки вікно очиститься
    print("\nОчікуємо 4 секунди...")
    time.sleep(4)

    print("\n=== Нова серія повідомлень після очікування ===")
    for message_id in range(11, 21):
        user_id = message_id % 5 + 1
        result = limiter.record_message(str(user_id))
        wait_time = limiter.time_until_next_allowed(str(user_id))
        print(f"Повідомлення {message_id:2d} | Користувач {user_id} | "
              f"{'✓' if result else f'× (очікування {wait_time:.1f}с)'}")
        # Випадкова затримка від 0.1 до 1 секунди
        time.sleep(random.uniform(0.1, 1.0))


if __name__ == "__main__":
    test_rate_limiter()

'''
=== Симуляція потоку повідомлень ===
Повідомлення  1 | Користувач 2 | ✓
Повідомлення  2 | Користувач 3 | ✓
Повідомлення  3 | Користувач 4 | ✓
Повідомлення  4 | Користувач 5 | ✓
Повідомлення  5 | Користувач 1 | ✓
Повідомлення  6 | Користувач 2 | × (очікування 8.2с)
Повідомлення  7 | Користувач 3 | × (очікування 8.1с)
Повідомлення  8 | Користувач 4 | × (очікування 8.0с)
Повідомлення  9 | Користувач 5 | × (очікування 7.5с)
Повідомлення 10 | Користувач 1 | × (очікування 7.3с)

Очікуємо 4 секунди...

=== Нова серія повідомлень після очікування ===
Повідомлення 11 | Користувач 2 | × (очікування 1.7с)
Повідомлення 12 | Користувач 3 | × (очікування 2.1с)
Повідомлення 13 | Користувач 4 | × (очікування 1.7с)
Повідомлення 14 | Користувач 5 | × (очікування 2.0с)
Повідомлення 15 | Користувач 1 | × (очікування 2.0с)
Повідомлення 16 | Користувач 2 | ✓
Повідомлення 17 | Користувач 3 | ✓
Повідомлення 18 | Користувач 4 | ✓
Повідомлення 19 | Користувач 5 | ✓
Повідомлення 20 | Користувач 1 | ✓
'''