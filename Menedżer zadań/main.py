import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import time

from SQLite import add_task, get_tasks, update_task, delete_task

def send_email(recipient, subject, body):
    sender_email = "ilchenkodmytro522@gmail.com"
    sender_password = "MyPassword"
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, recipient, message.as_string())
    server.quit()

def send_reminder():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    today = datetime.now().date()
    reminder_threshold = today + timedelta(days=1)
    cursor.execute('''
    SELECT id, name, deadline FROM tasks
    WHERE deadline <= ? AND notification_needed = 1
    ''', (reminder_threshold,))
    tasks = cursor.fetchall()
    for task in tasks:
        subject = "Przypomnienie o zadaniu"
        body = f"Przypomnienie: Zadanie '{task[1]}' (ID: {task[0]}) ma termin {task[2]}. Proszę pamiętać o jego wykonaniu!"
        send_email("recipient_email@gmail.com", subject, body)
    conn.close()

def display_tasks():
    tasks = get_tasks()
    if not tasks:
        print("Obecnie nie ma żadnych zadań.")
    else:
        for task in tasks:
            print(f"ID: {task[0]}, Nazwa: {task[1]}, Opis: {task[2]}, Priorytet: {task[3]}, Status: {task[4]}, Termin: {task[5]}, Przypomnienie: {'Tak' if task[6] else 'Nie'}")

def get_task_details():
    name = input("Wprowadź nazwę zadania: ")
    description = input("Wprowadź opis zadania: ")
    priority = input("Wprowadź priorytet zadania (liczba): ")
    status = input("Wprowadź status zadania: ")
    deadline = input("Wprowadź termin wykonania zadania (RRRR-MM-DD): ")
    notification_needed = input("Czy potrzebne przypomnienie? (1 - tak, 0 - nie): ")
    return (name, description, priority, status, deadline, notification_needed)

def update_task_details(task_id):
    print("Pozostaw pole puste, jeśli nie chcesz go zmieniać.")
    name = input("Wprowadź nową nazwę zadania: ")
    description = input("Wprowadź nowy opis zadania: ")
    priority = input("Wprowadź nowy priorytet zadania (liczba): ")
    status = input("Wprowadź nowy status zadania: ")
    deadline = input("Wprowadź nowy termin wykonania zadania (RRRR-MM-DD): ")
    notification_needed = input("Czy potrzebne przypomnienie? (1 - tak, 0 - nie): ")
    update_task(task_id, name if name else None, description if description else None, int(priority) if priority else None, status if status else None, deadline if deadline else None, int(notification_needed) if notification_needed else None)

def delete_task_by_id(task_id):
    delete_task(task_id)
    print(f"Zadanie o ID {task_id} zostało usunięte.")

def show_menu():
    print("\n1. Dodaj nowe zadanie")
    print("2. Przeglądaj zadania")
    print("3. Edytuj zadanie")
    print("4. Usuń zadanie")
    print("5. Wyjdź")
    choice = input("Wybierz opcję: ")
    return choice

def main():
    last_checked = datetime.now()
    check_interval = timedelta(hours=24)

    while True:
        if datetime.now() - last_checked > check_interval:
            send_reminder()
            last_checked = datetime.now()

        user_choice = show_menu()
        if user_choice == "1":
            details = get_task_details()
            add_task(*details)
        elif user_choice == "2":
            display_tasks()
        elif user_choice == "3":
            task_id = int(input("Wprowadź ID zadania, które chcesz zaktualizować: "))
            update_task_details(task_id)
        elif user_choice == "4":
            task_id = int(input("Wprowadź ID zadania, które chcesz usunąć: "))
            delete_task_by_id(task_id)
        elif user_choice == "5":
            print("Wyjście z programu...")
            break
        else:
            print("Nieprawidłowy wybór, spróbuj ponownie.")
        time.sleep(1)

if __name__ == "__main__":
    main()
