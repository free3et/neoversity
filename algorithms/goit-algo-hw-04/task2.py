import turtle

def koch_curve(t, order, size):
    if order == 0:
        t.forward(size)
    else:
        for angle in [60, -120, 60, 0]:
            koch_curve(t, order-1, size/3)
            t.left(angle)
            
def draw_koch_curve(order, size=300):
    window = turtle.Screen()
    window.bgcolor("white")
    window.title(f"Сніжинка Коха (Рівень: {order})")

    t = turtle.Turtle()
    t.speed(0)  
    t.penup()
    t.goto(-size / 2, size / 3)
    t.pendown()

    for _ in range(3):
        koch_curve(t, order, size)
        t.right(120)  # Поворот для наступної сторони трикутника

    window.mainloop()

if __name__ == "__main__":
    try:
        # Користувач вказує рівень рекурсії
        user_order = int(input("Введіть рівень рекурсії для сніжинки Коха (рекомендовано 0-4): "))
        
        if user_order < 0:
            print("Рівень рекурсії не може бути від'ємним. Встановлено рівень 0.")
            user_order = 0
            
        print("Малюємо фрактал... Закрийте вікно Turtle, щоб завершити програму.")
        draw_koch_curve(user_order)
        
    except ValueError:
        print("Помилка: Будь ласка, введіть коректне ціле число!")
