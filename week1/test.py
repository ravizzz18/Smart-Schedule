import sqlite3
from datetime import datetime
import openai

# -------------------------
# OpenAI API Setup
# -------------------------
openai.api_key = "YOUR_OPENAI_API_KEY"  # <-- Replace with your API key

def generate_ai_study_plan(student_name, special_needs):
    prompt = f"""
    Create a personalized study roadmap for a student named {student_name}.
    The student has the following learning needs: {special_needs}.
    Include:
    - Daily practice tips
    - Weekly schedule
    - Resources to use
    - Study strategies for difficult topics
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful educational assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300
    )

    return response.choices[0].message.content

# -------------------------
# Database Setup
# -------------------------
conn = sqlite3.connect("school.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    special_needs TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS teachers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    available_slots TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS classes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    teacher_id INTEGER,
    date TEXT,
    time TEXT,
    subject TEXT,
    FOREIGN KEY(student_id) REFERENCES students(id),
    FOREIGN KEY(teacher_id) REFERENCES teachers(id)
)
""")

conn.commit()

# -------------------------
# Management Functions
# -------------------------
def add_student():
    name = input("Enter student name: ")
    needs = input("Enter special learning needs (or leave blank): ")
    cursor.execute("INSERT INTO students (name, special_needs) VALUES (?, ?)", (name, needs))
    conn.commit()
    print(f"Student '{name}' added successfully!")

def add_teacher():
    name = input("Enter teacher name: ")
    slots = input("Enter available slots (e.g., Mon-Fri 10-12, 2-4): ")
    cursor.execute("INSERT INTO teachers (name, available_slots) VALUES (?, ?)", (name, slots))
    conn.commit()
    print(f"Teacher '{name}' added successfully!")

def list_students():
    cursor.execute("SELECT * FROM students")
    for s in cursor.fetchall():
        print(s)

def list_teachers():
    cursor.execute("SELECT * FROM teachers")
    for t in cursor.fetchall():
        print(t)

def is_slot_free(teacher_id, date, time):
    cursor.execute("SELECT * FROM classes WHERE teacher_id=? AND date=? AND time=?", (teacher_id, date, time))
    return cursor.fetchone() is None

def schedule_class():
    list_students()
    student_id = int(input("Enter student ID to schedule: "))
    list_teachers()
    teacher_id = int(input("Enter teacher ID: "))
    date = input("Enter date (YYYY-MM-DD): ")
    time = input("Enter time (HH:MM): ")
    subject = input("Enter subject: ")
    
    if is_slot_free(teacher_id, date, time):
        cursor.execute(
            "INSERT INTO classes (student_id, teacher_id, date, time, subject) VALUES (?, ?, ?, ?, ?)",
            (student_id, teacher_id, date, time, subject)
        )
        conn.commit()
        print(f"Class scheduled successfully!")
    else:
        print("Conflict detected: Teacher not available at this time.")

def generate_study_plan():
    list_students()
    student_id = int(input("Enter student ID to generate AI study plan: "))
    cursor.execute("SELECT name, special_needs FROM students WHERE id=?", (student_id,))
    student = cursor.fetchone()
    if student:
        name, needs = student
        plan = generate_ai_study_plan(name, needs)
        print("\n--- AI Study Plan ---")
        print(plan)
    else:
        print("Student not found.")

# -------------------------
# Main Menu
# -------------------------
def main():
    while True:
        print("\n--- Student Scheduling System ---")
        print("1. Add Student")
        print("2. Add Teacher")
        print("3. List Students")
        print("4. List Teachers")
        print("5. Schedule Class")
        print("6. Generate AI Study Plan")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_student()
        elif choice == "2":
            add_teacher()
        elif choice == "3":
            list_students()
        elif choice == "4":
            list_teachers()
        elif choice == "5":
            schedule_class()
        elif choice == "6":
            generate_study_plan()
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid choice! Try again.")

if _name_ == "_main_":
    main()