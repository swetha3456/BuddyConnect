import sqlite3

def init_db():
    with open("create_database.sql") as f:
        script = f.read()

    conn = sqlite3.connect("database.db", timeout=10)
    cursor = conn.cursor()
    cursor.executescript(script)
    conn.commit()
    conn.close()

def authenticate_user(username, password):
    conn = sqlite3.connect("database.db", timeout=10)
    cursor = conn.cursor()

    try:
        expected_password = list(cursor.execute(f"select password from users where username='{username}';"))[0][0]
    except:
        return False
    conn.close()

    return password == expected_password

def register_user(email, password, first_name, last_name, gender, location, interests):
    command = f"""insert into users(first_name, last_name, email, password, location, gender) values(
        '{first_name}',
        '{last_name}',
        '{email}',
        '{password}',
        '{location}',
        '{gender}'
    );"""

    conn = sqlite3.connect("database.db", timeout=10)
    cursor = conn.cursor()
    cursor.execute(command)

    for interest in interests:
        command = f"insert into user_interests values('{email}', '{interest}');"
        cursor.execute(command)

    conn.commit()
    conn.close()

def create_event(name, type, venue, location, date, start_time, end_time, user_email, desc):
    command = f"""insert into 
    events(event_name, event_type, venue, event_date, start_time, end_time, location, description, created_by) values(
        '{name}', '{type}', '{venue}', '{date}', '{start_time}', '{end_time}', '{location}', '{desc}', '{user_email}'
    );"""

    conn = sqlite3.connect("database.db", timeout=10)
    cursor = conn.cursor()
    cursor.execute(command)
    conn.commit()
    conn.close() 

def get_relevant_events(email):
    command = f"""select * from events
    where event_type in (select interest from user_interests where email='{email}')
    and event_date >= DATE('now') and location = (select location from users where email='{email}')
    order by event_date desc;"""

    conn = sqlite3.connect("database.db", timeout=10)
    cursor = conn.cursor()
    cursor.execute(command)
    result = cursor.fetchall()
    conn.close()

    return result

def get_user_location(user_email):
    conn = sqlite3.connect("database.db", timeout=10)
    cursor = conn.cursor()
    cursor.execute(f"select location from users where email='{user_email}'")
    location = cursor.fetchone()[0]
    conn.close()

    return location

def get_full_name(user_email):
    conn = sqlite3.connect("database.db", timeout=10)
    cursor = conn.cursor()
    cursor.execute(f"select concat(first_name, ' ', last_name) from users where email='{user_email}'")
    name = cursor.fetchone()[0]
    conn.close()

    return name

if __name__ == "__main__":
    init_db()