import time
from typing import Dict
import random


class ThrottlingRateLimiter:
    def __init__(self, min_interval: float = 10.0):
        self.min_interval = min_interval
        # user_id - час останнього прийнятого повідомлення
        self.last_message_time: Dict[str, float] = {}

    def can_send_message(self, user_id: str) -> bool:
        # Перевіряє, чи минуло min_interval секунд від останнього повідомлення
        last_time = self.last_message_time.get(user_id)
        # Перше повідомлення від користувача — завжди дозволено
        if last_time is None:
            return True
        return time.time() - last_time >= self.min_interval

    def record_message(self, user_id: str) -> bool:
        # Записує повідомлення, якщо інтервал дотримано. Повертає True, якщо повідомлення прийнято, інакше False
        if not self.can_send_message(user_id):
            return False
        self.last_message_time[user_id] = time.time()
        return True

    def time_until_next_allowed(self, user_id: str) -> float:
        # Повертає час очікування (у секундах) до наступного дозволеного повідомлення. 0.0 — якщо можна надсилати вже зараз
        last_time = self.last_message_time.get(user_id)
        if last_time is None:
            return 0.0
        wait = last_time + self.min_interval - time.time()
        return max(0.0, wait)


def test_throttling_limiter():
    limiter = ThrottlingRateLimiter(min_interval=10.0)

    print("\n=== Симуляція потоку повідомлень (Throttling) ===")
    for message_id in range(1, 11):
        user_id = message_id % 5 + 1

        result = limiter.record_message(str(user_id))
        wait_time = limiter.time_until_next_allowed(str(user_id))

        print(f"Повідомлення {message_id:2d} | Користувач {user_id} | "
              f"{'✓' if result else f'× (очікування {wait_time:.1f}с)'}")

        # Випадкова затримка між повідомленнями
        time.sleep(random.uniform(0.1, 1.0))

    print("\nОчікуємо 10 секунд...")
    time.sleep(10)

    print("\n=== Нова серія повідомлень після очікування ===")
    for message_id in range(11, 21):
        user_id = message_id % 5 + 1
        result = limiter.record_message(str(user_id))
        wait_time = limiter.time_until_next_allowed(str(user_id))
        print(f"Повідомлення {message_id:2d} | Користувач {user_id} | "
              f"{'✓' if result else f'× (очікування {wait_time:.1f}с)'}")
        time.sleep(random.uniform(0.1, 1.0))


if __name__ == "__main__":
    test_throttling_limiter()

'''
=== Симуляція потоку повідомлень (Throttling) ===
Повідомлення  1 | Користувач 2 | ✓
Повідомлення  2 | Користувач 3 | ✓
Повідомлення  3 | Користувач 4 | ✓
Повідомлення  4 | Користувач 5 | ✓
Повідомлення  5 | Користувач 1 | ✓
Повідомлення  6 | Користувач 2 | × (очікування 6.8с)
Повідомлення  7 | Користувач 3 | × (очікування 6.5с)
Повідомлення  8 | Користувач 4 | × (очікування 6.5с)
Повідомлення  9 | Користувач 5 | × (очікування 6.6с)
Повідомлення 10 | Користувач 1 | × (очікування 7.0с)

Очікуємо 10 секунд...

=== Нова серія повідомлень після очікування ===
Повідомлення 11 | Користувач 2 | ✓
Повідомлення 12 | Користувач 3 | ✓
Повідомлення 13 | Користувач 4 | ✓
Повідомлення 14 | Користувач 5 | ✓
Повідомлення 15 | Користувач 1 | ✓
Повідомлення 16 | Користувач 2 | × (очікування 7.4с)
Повідомлення 17 | Користувач 3 | × (очікування 7.6с)
Повідомлення 18 | Користувач 4 | × (очікування 7.8с)
Повідомлення 19 | Користувач 5 | × (очікування 8.3с)
Повідомлення 20 | Користувач 1 | × (очікування 8.3с)
'''