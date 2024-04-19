import sqlite3

def add_task(name, description, priority, status, deadline, notification_needed):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO tasks (name, description, priority, status, deadline, notification_needed)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, description, priority, status, deadline, notification_needed))

    conn.commit()
    conn.close()
    print('Nowe zadanie zostało pomyślnie dodane.')

def get_tasks():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()

    conn.close()
    return tasks

def update_task(id, name=None, description=None, priority=None, status=None, deadline=None, notification_needed=None):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()

    fields = []
    params = []
    if name is not None:
        fields.append("name = ?")
        params.append(name)
    if description is not None:
        fields.append("description = ?")
        params.append(description)
    if priority is not None:
        fields.append("priority = ?")
        params.append(priority)
    if status is not None:
        fields.append("status = ?")
        params.append(status)
    if deadline is not None:
        fields.append("deadline = ?")
        params.append(deadline)
    if notification_needed is not None:
        fields.append("notification_needed = ?")
        params.append(notification_needed)

    params.append(id)
    update_stmt = "UPDATE tasks SET " + ", ".join(fields) + " WHERE id = ?"
    cursor.execute(update_stmt, params)

    conn.commit()
    conn.close()

def delete_task(id):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tasks WHERE id = ?", (id,))

    conn.commit()
    conn.close()
