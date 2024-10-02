import requests
import matplotlib.pyplot as plt
import pandas as pd

# Задаємо діапазон дат
dates = pd.date_range("2024-09-23", "2024-09-29")

# Словник для зберігання курсів валют
exchange_rates = {"date": [], "USD": [], "EUR": []}

# Отримуємо дані для кожної дати в діапазоні
for date in dates:
    formatted_date = date.strftime("%Y%m%d")  # Форматуємо дату як YYYYMMDD
    url = f"https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?date={formatted_date}&json"

    # Запит до API НБУ
    response = requests.get(url)
    data = response.json()

    # Знаходимо курси валют USD та EUR
    usd_rate = next(item['rate'] for item in data if item['cc'] == 'USD')
    eur_rate = next(item['rate'] for item in data if item['cc'] == 'EUR')

    # Додаємо дані до словника
    exchange_rates["date"].append(date)
    exchange_rates["USD"].append(usd_rate)
    exchange_rates["EUR"].append(eur_rate)

# Перетворюємо словник у DataFrame для зручності роботи з даними
df = pd.DataFrame(exchange_rates)

# Побудова графіка
plt.figure(figsize=(12, 6))

# Стиль для графіку
plt.style.use('ggplot')  # Використання стилю ggplot для візуального покращення

# Додавання графіків для USD та EUR з маркерами
plt.plot(df['date'], df['USD'], marker='o', linestyle='-', color='blue', label='USD', linewidth=2)
plt.plot(df['date'], df['EUR'], marker='o', linestyle='--', color='orange', label='EUR', linewidth=2)

# Додавання міток для кожного значення
for i, (date, usd, eur) in enumerate(zip(df['date'], df['USD'], df['EUR'])):
    plt.text(date, usd + 0.05, f'{usd:.2f}', ha='center', va='bottom', fontsize=9, color='blue')  # USD мітка
    plt.text(date, eur - 0.05, f'{eur:.2f}', ha='center', va='top', fontsize=9, color='orange')  # EUR мітка

# Виділення максимальних і мінімальних значень
max_usd = df['USD'].max()
min_usd = df['USD'].min()
max_eur = df['EUR'].max()
min_eur = df['EUR'].min()


# Налаштування графіка
plt.xlabel('Дата', fontsize=12)
plt.ylabel('Курс', fontsize=12)
plt.title('Зміна курсів валют (23.09.2024 - 29.09.2024)', fontsize=16)
plt.xticks(rotation=45)  # Повертаємо дати для кращого вигляду
plt.legend(fontsize=12)
plt.grid(True)
plt.tight_layout()

# Показуємо графік
plt.show()
