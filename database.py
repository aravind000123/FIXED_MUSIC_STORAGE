import sqlite3

conn = sqlite3.connect("usersongs.db")

cursor = conn.cursor()

cursor.execute('''select password,fname from users_table where email = ?''',("gelamaravind@gmail.com",))
# output is getting in the TUPLE format for output so using like output[0]
output = cursor.fetchone()
if output == None:
    print("not there!")
print(output)
conn.commit()
conn.close()