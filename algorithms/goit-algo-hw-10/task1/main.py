import timeit

coins = [50, 25, 10, 5, 2, 1]

def find_coins_greedy(amount):
  result = {}
  for coin in coins:
    if amount >= coin:
      result[coin] = amount // coin
      amount %= coin
  return result

def find_min_coins(amount):
  result = {}
  dp = [float('inf')] * (amount + 1) # заповнюємо всі комірки значенням "нескінченність" (float('inf')
  dp[0] = 0 # для суми 0 потрібно 0 монет
  coin_used = [0] * (amount + 1) # зберігатиме номінал останньої монети, використаної для суми i
  for i in range(1, amount + 1):
    for coin in coins:
      if coin <= i: # Перевіряємо, чи дає ця монета меншу загальну кількість монет
        if dp[i - coin] + 1 < dp[i]:
          dp[i] = dp[i - coin] + 1
          coin_used[i] = coin  # Запам'ятовуємо монету
  current_amount = amount
  # Відстежуємо монети у зворотному порядку, поки сума не стане 0
  while current_amount > 0:
    coin = coin_used[current_amount]
    if coin in result:
        result[coin] += 1
    else:
        result[coin] = 1
    # Віднімаємо монету від поточної суми
    current_amount -= coin
  return result

print(find_coins_greedy(113))
print(find_min_coins(113))

# Порівняння ефективності алгоритмів на різних сумах
REPEATS = 10

for amount in [100, 1_000, 10_000, 50_000]:
    greedy_time = timeit.timeit(lambda a=amount: find_coins_greedy(a), number=REPEATS)
    dp_time = timeit.timeit(lambda a=amount: find_min_coins(a), number=REPEATS)
    print(f"--- amount={amount}, repeats={REPEATS} ---")
    print('find_coins_greedy >>>', f'{greedy_time:.8f}')
    print('find_min_coins >>>', f'{dp_time:.8f}')
    print('--------------------------------')