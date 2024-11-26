import sqlite3

connection = sqlite3.connect('not_telegram.db')
cursor = connection.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL)
''')
# count = 10
# for i in range(10):
#     cursor.execute('INSERT INTO Users (username, email, age, balance) VALUES (?,?,?,?)',(f'User{i+1}',
#     f'example{i+1}@gmail.com', count, 1000))
#     count += 10
#
#
# count2 = 1
# for i in range(10):
#     cursor.execute('UPDATE Users SET balance = ? WHERE id = ? ', (500, count2))
#     count2+=2
#
# count3 = 1
# for i in range(10):
#     cursor.execute('DELETE FROM Users WHERE id = ? ', (count3,))
#     count3+=3
#
# cursor.execute('SELECT username, email, age, balance FROM Users WHERE age != 60')
# users = cursor.fetchall()
# print('Имя:',users[0][0], '|', 'Почта:',users[0][1],'|', 'Возраст:',users[0][2],'|', 'Баланс:', users[0][3])
# print('Имя:',users[1][0],'|', 'Почта:',users[1][1],'|', 'Возраст:',users[1][2],'|', 'Баланс:', users[1][3])
# print('Имя:',users[2][0], '|','Почта:',users[2][1],'|', 'Возраст:',users[2][2],'|', 'Баланс:', users[2][3])
# print('Имя:',users[3][0],'|', 'Почта:',users[3][1], '|','Возраст:',users[3][2],'|', 'Баланс:', users[3][3])
# print('Имя:',users[4][0],'|', 'Почта:',users[4][1],'|', 'Возраст:',users[4][2],'|', 'Баланс:', users[4][3])

cursor.execute('DELETE FROM Users WHERE id = 6')
cursor.execute('SELECT COUNT(*) FROM Users')
tot = cursor.fetchone()[0]
cursor.execute('SELECT SUM(balance) FROM Users')
sum_of_balance = cursor.fetchone()[0]
print(sum_of_balance/tot)



connection.commit()
connection.close()