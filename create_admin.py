from infosystem import DataBase

db = DataBase()

username = 'admin'
password = 'admin'

db.add_user(username, password, 'admin')
if db.check_user(username, password):
    print('User created successfully or already exists')
else:
    print('Error')