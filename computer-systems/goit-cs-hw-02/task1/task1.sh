#!/bin/bash
log_file="website_status.log"

sites=("https://google.com" "https://facebook.com" "https://twitter.com" "https://google1.com")
for site in "${sites[@]}"; do
    # щоб отримати чисту відповідь:
    # -s (silent) — ховає помилки
    # -L для опрацювання редиректів
    # -o /dev/null — ігнорує тіло відповіді (нам потрібен лише код відповіді)
    # -w "%{http_code}" — виводить лише HTTP-код відповіді
    # --max-time 5 — таймаут 5 секунд, щоб скрипт не зависав
    response=$(curl -s -L -o /dev/null -w "%{http_code}" --max-time 5 "$site")

    # Перевіряємо, чи дорівнює статус-код 200
    if [ "$response" -eq 200 ]; then
        echo "$site is UP" >> "$log_file"
    else
        echo "$site is DOWN" >> "$log_file"
    fi
done
echo "Результати успішно збережено у файл: $log_file"