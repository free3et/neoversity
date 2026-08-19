import random
import matplotlib.pyplot as plt
import numpy as np
import scipy.integrate as spi

# Функція, площу під якою шукаємо: f(x) = x^2
def f(x):
    return x ** 2

a = 0  # ліва межа інтеграла
b = 2  # права межа інтеграла

# графік: сіра зона = площа, яку оцінюємо
x = np.linspace(-0.5, 2.5, 400)
y = f(x)

fig, ax = plt.subplots()
ax.plot(x, y, 'r', linewidth=2)

# сіра заливка — інтеграл від a до b
ix = np.linspace(a, b)
iy = f(ix)
ax.fill_between(ix, iy, color='gray', alpha=0.3)

ax.set_xlim([x[0], x[-1]])
ax.set_ylim([0, max(y) + 0.1])
ax.set_xlabel('x')
ax.set_ylabel('f(x)')
ax.axvline(x=a, color='gray', linestyle='--')
ax.axvline(x=b, color='gray', linestyle='--')
ax.set_title('Графік інтегрування f(x) = x^2 від ' + str(a) + ' до ' + str(b))
plt.grid()
plt.show()


def is_inside(x, y):
    # Точка потрапила в сіру зону, якщо вона не вище кривої
    return y <= f(x)


def monte_carlo_integral(a, b, num_points):
    # Прямокутник, у який кидаємо точки:
    # ширина = (b - a), висота = f(b) = 4, бо 2^2 = 4
    y_max = f(b)
    rect_area = (b - a) * y_max

    # N випадкових точок у цьому прямокутнику
    points = [(random.uniform(a, b), random.uniform(0, y_max)) for _ in range(num_points)]

    # M — скільки з них опинились під кривою (у сірій зоні)
    inside_points = [point for point in points if is_inside(point[0], point[1])]
    M = len(inside_points)
    N = len(points)

    # Частка точок під кривою * площа прямокутника ≈ площа сірої зони
    return (M / N) * rect_area

analytical = (b ** 3 - a ** 3) / 3

# Те саме число через бібліотеку SciPy (функція quad)
quad_result, quad_error = spi.quad(f, a, b)

print(f"Аналітичний інтеграл: {analytical}")
print(f"Інтеграл quad: {quad_result} (похибка {quad_error})")
print()
print(f"{'Точок':>8} | {'Монте-Карло':>12} | {'Похибка':>10}")

# Більше точок — зазвичай менша похибка (але результат випадковий)
for num_points in [1_000, 10_000, 100_000]:
    mc_result = monte_carlo_integral(a, b, num_points)
    error = abs(mc_result - analytical)
    print(f"{num_points:>8} | {mc_result:12.6f} | {error:10.6f}")
