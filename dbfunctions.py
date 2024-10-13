import sqlite3

def init_db():
    with open("create_database.sql") as f:
        script = f.read()

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.executescript(script)
    conn.commit()
    conn.close()

def authenticate_user(username, password):
    conn = sqlite3.connect("database.db")
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

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(command)

    for interest in interests:
        command = f"insert into user_interests values('{email}', '{interest}');"
        cursor.execute(command)

    conn.commit()
    conn.close()

def create_event(name, type, venue, location, date, start_time, end_time, user_email):
    command = f"""insert into 
    events(event_name, event_type, venue, event_date, start_time, end_time, location, created_by) values(
        '{name}', '{type}', '{venue}', {date}, {start_time}, {end_time}, '{location}', {user_email}'
    );"""

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(command)
    conn.commit()
    conn.close() 

def get_relevant_events(email):
    command = f"""select * from events
    where event_type in (select interest from user_interests where email='{email}')
    and event_date >= now() and location = (select location from users where where email='{email}')
    sort by event_date desc;"""

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    result = cursor.execute(command)
    conn.close()

    return result

def send_request(event_id, requesting_user):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("insert into user_requests(event_id, user_email) values('{event_id}', '{requesting_user}')")
    conn.commit()
    conn.close()

def accept_request(event_id, requesting_user):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("update user_requests set status='ACCEPTED' where event_id='{event_id}' and user_email='{requesting_user}'")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()