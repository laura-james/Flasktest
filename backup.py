
con = sqlite3.connect('users.db')
cursor = con.cursor()
sql2 = '''
        CREATE TABLE `users` (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        `username` varchar(40) NOT NULL,
        `password` varchar(30) NOT NULL,
        `email_address` varchar(20) NOT NULL,
        `first_name` varchar(20),      
        `last_name` varchar(20)
)
  '''
#cursor.execute(sql2)
con.commit()

sql1 = '''
INSERT INTO users(username,password,email_address,first_name,last_name) VALUES ("Deadpool2","haha2","dead@pool.com","Ryan2","Reynolds");
'''
cursor.execute(sql1)
con.commit()
sql = '''
      SELECT * FROM users 
      '''
cursor.execute(sql)
con.commit()

rows = cursor.fetchall() 
for row in rows:
    print(row)