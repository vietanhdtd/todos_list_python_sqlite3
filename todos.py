import os  
import sqlite3
import fire
from datetime import datetime 



DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'database.sqlite3')

conn = sqlite3.connect(DEFAULT_PATH)
cur = conn.cursor()

sql = """
    CREATE TABLE IF NOT EXISTS todos(
        id INTEGER PRIMARY KEY,
        todo_text TEXT NOT NULL,
        time_create TEXT NOT NULL,
        due_date TEXT DEFAULT NULL,
        project_id TEXT DEFAULT NULL,
        user_id TEXT DEFAULT NULL,
        todo_status TEXT NOT NULL DEFAULT "incomplete"
    );
"""
cur.execute(sql)

sql = """
    CREATE TABLE IF NOT EXISTS project(
        id INTEGER PRIMARY KEY,
        project_name TEXT NOT NULL
    )
"""
cur.execute(sql)
sql = """
    CREATE TABLE IF NOT EXISTS user(
        id INTEGER PRIMARY KEY,
        user_name TEXT NOT NULL,
        email_address TEXT NOT NULL
    )
"""
cur.execute(sql)
conn.commit()


def add_todo():
    todo_text = input()
    print("adding todo now!")
    sql = """
        INSERT INTO todos (todo_text, time_create) VALUES (?, ?)
    """
    cur.execute(sql, (todo_text, datetime.now().strftime("%d-%m-%Y %H:%M")))
    print(todo_text + " *has been added*")
    conn.commit()


def mark_complete():
    todo_id = input("")
    sql = """
        UPDATE todos SET todo_status = "completed" WHERE id = ?
    """
    print("To do has been marked completed")  
    cur.execute(sql, (todo_id,))
    conn.commit()

def add_project_id():
    project_id = input("Choose your Project_ID: ")
    idx = input("To do ID: ")
    sql = """
        UPDATE todos SET project_id = ? WHERE id = ?
    """
    print("Project ID has been added")  
    cur.execute(sql, (project_id,idx))
    conn.commit()

def add_user_id():
    user_id = input("Choose your User_ID: ")
    idx = input("To do ID: ")
    sql = """
        UPDATE todos SET user_id = ? WHERE id = ?
    """
    print("User ID has been added")  
    cur.execute(sql, (user_id,idx))
    conn.commit()

def list():
    print("1. List all todos\n"
        "2. List all Users\n"
        "3. List all Projects\n"
        "4. List Completed or incomplete todos\n"
        "5. List todos via Projects_ID")
    search = str(input("---->"))
    if search == "1":
        sql = """
            SELECT * FROM todos
        """
        cur.execute(sql)
    elif search == "2":
        sql = """
            SELECT * FROM user
        """
        cur.execute(sql)
    elif search == "3":
        sql = """
            SELECT * FROM project
        """
        cur.execute(sql)
    elif search == "4":
        value = input("Completed or Incomplete: ")
        sort = input("Sort By(desc/asc): ")
        sql = """
            SELECT id,todo_text,due_date,todo_status FROM todos WHERE todo_status = ? ORDER BY due_date {}
        """.format(sort)
        cur.execute(sql,(value,))     
    else:
        value = input("Choose your Project_ID: ")
        sort = input("Sort By(desc/asc): ")
        sql = """
            SELECT * FROM todos WHERE project_id = ? ORDER BY due_date {}
        """.format(sort)
        cur.execute(sql, (value,))

    conn.commit()
    print("Todos List: ")
    results = cur.fetchall()
    for row in results:
        print(row)

def add_project():
    name = input("Insert your Project's name: ")
    print("adding project Name now!")
    sql = """
        INSERT INTO project (project_name) VALUES (?)
    """
    cur.execute(sql,(name,))
    print(name + " *has been added*")
    conn.commit()

def add_user():
    name = input("Insert user name: ")
    email = input("Email Address: ")
    print("adding user_info now!")
    sql= """
        INSERT INTO user (user_name, email_address) VALUES (?,?)
    """
    cur.execute(sql,(name,email))
    print(" *User Info has been added*")
    conn.commit()
    

def staff():
    print("loading...")
    sql="""
        SELECT DISTINCT project_name,user_name FROM todos
        LEFT JOIN user 
        ON todos.user_id = user.id
        LEFT JOIN project 
        ON todos.project_id = project.id
    """
    cur.execute(sql)
    results = cur.fetchall()
    for row in results:
        print(row)


def who_to_fire():
    sql="""
        SELECT user_name,email_address FROM user
        LEFT JOIN todos 
        ON user.id = todos.user_id
        WHERE todo_text is NULL
    """
    cur.execute(sql)
    results = cur.fetchall()
    for row in results:
        print(row)


if __name__ == '__main__':
    fire.Fire({
        'add_todo': add_todo,
        'list': list,
        'mark_complete': mark_complete,
        'add_project': add_project,
        'add_user': add_user,
        'staff': staff,
        'add_project_id':add_project_id,
        'add_user_id':add_user_id,
        'who_to_fire': who_to_fire 
})  

conn.close()