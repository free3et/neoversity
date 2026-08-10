import math
import turtle

def pythagoras_tree(t, size, level):
    if level == 0:
        return
    t.forward(size) # малюємо стовбур дерева на відстань size

    t.left(45)
    pythagoras_tree(t, size * math.sqrt(2) / 2, level-1) # малюємо ліву гілку

    t.right(90)
    pythagoras_tree(t, size * math.sqrt(2) / 2, level-1) # малюємо праву гілку

    t.left(45)
    t.backward(size) # повертаємося назад на відстань size
    
            
def draw_pythagoras_tree(order, size=200):
    window = turtle.Screen()
    window.bgcolor("white")
    window.title(f"Дерево Піфагора (Рівень: {order})")

    t = turtle.Turtle() 
    t.speed(0)  
    t.left(90)
    t.penup()
    t.goto(0, -150) # переміщуємо вниз на 150 пікселів
    t.pendown()

    pythagoras_tree(t, size, order)

    window.mainloop()

if __name__ == "__main__":
    try:
        # Користувач вказує рівень рекурсії
        user_order = int(input("Введіть рівень рекурсії для дерева Піфагора (рекомендовано 0-4): "))
        
        if user_order < 0:
            print("Рівень рекурсії не може бути від'ємним. Встановлено рівень 0.")
            user_order = 0
            
        print("Малюємо дерево Піфагора... Закрийте вікно Turtle, щоб завершити програму.")
        draw_pythagoras_tree(user_order)
        
    except ValueError:
        print("Помилка: Будь ласка, введіть коректне ціле число!")
