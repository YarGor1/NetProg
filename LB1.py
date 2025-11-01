# ЗАВДАННЯ 1

# Курс Євро із сайту НБУ за попередній тиждень за допомогою Postman
url_api = "https://bank.gov.ua/NBU_Exchange/exchange_site?&json&valcode=eur&start=20251020&end=20251026"

print("""
===============================================================================================
===============================================================================================
===============================================================================================
""")

# ЗАВДАННЯ 2

import requests

api = requests.get(url_api)
currency = api.json()

for i in currency: # Вивід інформації щодо курсу Євро у python
    print(i)

print("""
===============================================================================================
===============================================================================================
===============================================================================================
""")

# ЗАВДАННЯ 3

import matplotlib.pyplot as plt

time = []
val = []

for i in currency:
    time.append(i['exchangedate']) # Експорт даних про час
    val.append(i['rate'])          # Експорт даних про вартість

fig, ax = plt.subplots()
ax.plot(time, val)
ax.grid(True, linestyle='-.')
ax.tick_params(labelcolor='r', labelsize='medium', width=3)
plt.title('КУРС ЄВРО')
plt.scatter(time, val)

plt.show() #Вивід графіку

print("""
===============================================================================================
===============================================================================================
===============================================================================================
""")

# ЗАВДАННЯ 4

from telethon import TelegramClient

# Використайте свої дані для авторизації!
api_id = 12345
api_hash = '0123456789abcdef0123456789abcdef'
client = TelegramClient('anon', api_id, api_hash)

async def main():
    
    ### Написати повідомлення користувачу
#    await client.send_message('@Friend_nickname', 'Hello, my friend!') 

    # Надати інформацію про всі чати
#    async for dialog in client.iter_dialogs():
#        print(dialog.name, 'has ID', dialog.id)

    # Перелік користувачів чату    
    group_username = "MyChat"   # Надайте ім'я чату. Точну назву можна отримати з попереднього циклу про всі чати
    entity = await client.get_entity(group_username)
    print(f"ID чату: {entity.id}")
    print("Отримання користувачів чату...")

    participants_count = 0
    # Надання інформації про кожного користувача
    async for user in client.iter_participants(entity, aggressive=True):
        participants_count += 1
        print(f"ID: {user.id}, Имя: {user.first_name} {user.last_name or ''}, Username: {user.username or 'N/A'}")

    print(f"\nЗагальна кількість користувачів: {participants_count}")


with client:
    client.loop.run_until_complete(main())
