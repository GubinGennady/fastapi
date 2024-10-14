import MySQLdb

DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = '12345'
DB_NAME = 'fastapi1'

def get_connection():
    con = MySQLdb.connect(
        host=DB_HOST,
        user=DB_USER,
        passwd=DB_PASSWORD,
        db=DB_NAME
    )
    return con


def reg(login, password):
    con = get_connection()
    cursor = con.cursor()
    cursor.execute(f"insert into users_new  (login, password) values ('{login}', '{password}')")
    con.commit()

def auth(login, password):
    con = get_connection()
    cursor = con.cursor()
    cursor.execute(f"select * from users_new where login = '{login}' and password = '{password}'")
    print(cursor.fetchone())

def get_hash(login):
    con = get_connection()
    cursor = con.cursor()
    cursor.execute(f"select password from users_new where login = '{login}'")
    return cursor.fetchone()[0]

def get_vebinars():
    con = get_connection()
    cursor = con.cursor()
    #sql иньекция
    cursor.execute('select * from vebinars')
    return cursor.fetchall()