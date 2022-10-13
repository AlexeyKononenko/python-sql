
from pprint import pprint
import psycopg2



conn = psycopg2.connect(database="client_info", user="postgres", password="2707941325")
cur = conn.cursor()

def create_table(cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS clients(
    id SERIAL PRIMARY KEY, 
    name VARCHAR(100) NOT NULL, 
    surname VARCHAR(100) NOT NULL, 
    email VARCHAR(100) NOT NULL
    );
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS client_phonenumbers(
    id_phone SERIAL PRIMARY KEY,
    client_id INTEGER NOT NULL REFERENCES clients(id),
    client_phonenumber VARCHAR(20) UNIQUE);
    """)
    conn.commit()

def add_client(cur, name, surname, email):
    cur.execute(''' insert into clients(name, surname, email) values(%s, %s, %s)
    ''',(name, surname, email))
    conn.commit()

def add_phone(cur, client_id, client_phonenumber):
    cur.execute('''insert into client_phonenumbers(client_id, client_phonenumber) values(%s, %s)''', (client_id, client_phonenumber))
    conn.commit()

def change_info(cur):
    print('''Меню изменения данных клиета
    1. Изменить имя.
    2. Изменить фамилию.
    3.Измнить почту.
    4. Изменить телефон''')
    comand = int(input())
    if comand == 1:
        input_id = input('Введите ИД клиента: ')
        input_name = input('Введите новое имя клиента: ')
        cur.execute('''update clients set name = %s where id = %s;''', (input_name, input_id))
    elif comand ==2:
        input_id = input('Введите ИД клиента: ')
        surname_input = input('Введите новую фамилию: ')
        cur.execute('''update clients set surname = %s where id = %s;''', (surname_input, input_id))
    elif comand == 3:
        input_id = input('Введите ИД клиента: ')
        email_input = input('Введите новую почту: ')
        cur.execute('''update clients set email = %s where id = %s;''', (email_input, input_id))
    elif comand ==4:
        input_id = input('Введите ИД клиента: ')
        phone_input = input('Введите новый телефон: ')
        cur.execute('''update client_phonenumbers set client_phonenumber = %s where client_id = %s;''', (phone_input, input_id))           
    conn.commit()

def delete_phone(cur):
    id_input = input('Введите ИД клиета: ')
    phone_input = input('Введите номер телефона который нужно удалить: ')
    cur.execute('''delete from client_phonenumbers where client_id = %s and client_phonenumber = %s''', (id_input, phone_input) )
    conn.commit()

def del_client(cur):
    client_id = input('Введите ИД клиента: ')
    cur.execute("DELETE FROM clients WHERE id = %s;", (client_id))
    cur.execute("DELETE FROM client_phonenumbers WHERE client_id = %s;", (client_id))
    conn.commit()

def find_client(cur, name=None, surname=None, email=None,  client_phonenumber=None):
    if client_phonenumber is not None:
        cur.execute("""
            SELECT id FROM clients 
            JOIN client_phonenumbers ON client_phonenumbers.client_id = clients.id
            WHERE client_phonenumbers.client_phonenumber=%s;
            """, (client_phonenumber))
    else:
        cur.execute("""
            SELECT id FROM clients 
            WHERE name=%s OR surname=%s OR email=%s returning name, surname, email;
            """, (name, surname, email))
    print(cur.fetchall()) 

create_table(cur)

#add_client(cur, 'Dima', 'Orlov', '56746@mail.ru')
#add_client(cur, 'Ira', 'Maksimova', '56746@mail.ru')
#add_client(cur, 'Vadim', 'Mironov', 'mirn.ov@mail.ru')

#add_phone(cur, '2', '+7946231611')
#add_phone(cur, '3', '+799984135')
#add_phone(cur, '2', '+989789479')

#change_info(cur)

#delete_phone(cur)

find_client(cur, 'Vadim')

#del_client(cur)
conn.close