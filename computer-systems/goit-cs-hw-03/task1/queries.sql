-- 1. Отримати всі завдання певного користувача
-- =========================================
SELECT *
FROM tasks
WHERE user_id = 1;

-- 2. Вибрати завдання за певним статусом
-- =========================================
SELECT *
FROM tasks
WHERE status_id = (
    SELECT id
    FROM status
    WHERE name = 'new'
);

-- 3. Оновити статус конкретного завдання
-- =========================================
UPDATE tasks
SET status_id = (
    SELECT id
    FROM status
    WHERE name = 'in progress'
)
WHERE id = 2;

-- 4. Отримати список користувачів, які не мають жодного завдання
-- =========================================
SELECT *
FROM tasks
WHERE id NOT IN (
    SELECT user_id
    FROM tasks
);

-- 5. Додати нове завдання для конкретного користувача
-- =========================================
INSERT INTO tasks (id, title, description, status_id, user_id)
VALUES (34, 'hello world', 'say hello world', 2, 10);

-- 6. Отримати всі завдання, які ще не завершено
-- =========================================
SELECT *
FROM tasks
WHERE NOT status_id = (
    SELECT id
    FROM status
    WHERE name = 'completed'
);

-- 7. Видалити конкретне завдання
-- =========================================
DELETE FROM tasks
WHERE id = 3;

-- 8. Знайти користувачів з певною електронною поштою
-- =========================================
SELECT email
FROM users
WHERE email LIKE '%test%'

-- 9. Оновити ім'я користувача
-- =========================================
UPDATE users
SET fullname = 'Тарас Шевченко'
WHERE id = 4

-- 10. Отримати кількість завдань для кожного статусу
-- Використайте SELECT, COUNT, GROUP BY для групування завдань за статусами.
-- =========================================
SELECT
    status.name,
    COUNT(tasks.id) AS tasks_count
FROM status
JOIN tasks ON status.id = tasks.status_id
GROUP BY status.id, status.name;

-- 11. Отримати завдання, які призначені користувачам з певною доменною частиною електронної пошти.
-- =========================================
SELECT *
FROM tasks
JOIN users ON users.id = tasks.user_id
WHERE users.email LIKE '%@example.com%'

-- 12. Отримати список завдань, що не мають опису. Виберіть завдання, у яких відсутній опис.
-- =========================================
SELECT
    tasks.id,
    tasks.title,
    tasks.description
FROM tasks
WHERE tasks.description IS NULL

-- 13. Вибрати користувачів та їхні завдання, які є у статусі 'in progress'. Використайте INNER JOIN для отримання списку користувачів та їхніх завдань із певним статусом.
-- =========================================
SELECT
    users.id,
    users.fullname,
    users.email,
    tasks.id AS task_id,
    tasks.title,
    tasks.description,
    status.name AS status_name
FROM users
INNER JOIN tasks ON users.id = tasks.user_id
INNER JOIN status ON tasks.status_id = status.id 
WHERE status.name  = 'in progress'

-- 14. Отримати користувачів та кількість їхніх завдань. Використайте LEFT JOIN та GROUP BY для вибору користувачів та підрахунку їхніх завдань.
-- =========================================
SELECT
    users.fullname,
    users.email,
    COUNT(tasks.id) AS tasks_count
FROM users
LEFT JOIN tasks ON users.id = tasks.user_id
GROUP BY tasks.id, users.fullname, users.email;