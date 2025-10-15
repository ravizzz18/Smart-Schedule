import sqlite3
from datetime import datetime
import textwrap

def generate_ai_study_plan(student_name, special_needs):
    
    needs_summary = special_needs if special_needs else "General focus on foundational concepts."
    
    plan_template = f"""
    --- Personalized Study Roadmap for {student_name} ---

    Learning Focus: {needs_summary}

    ### 1. Daily Practice Tips
    * **Focus Intervals:** Use the Pomodoro Technique (25 minutes of work, 5 minutes break).
    * **Review:** Spend the first 10 minutes of study time reviewing yesterday's material.
    * **Active Recall:** Test yourself frequently using flashcards or practice questions.
    * **Movement:** Take a short walk or stretch every hour to reset focus.

    ### 2. Weekly Schedule Structure
    | Day | Morning Focus (9am-12pm) | Afternoon Focus (2pm-5pm) | Evening Review (7pm-8pm) |
    |-----|---------------------------|----------------------------|--------------------------|
    | Mon | Math/Science Deep Dive | Homework Application | Plan next day's tasks |
    | Tue | Language Arts/Reading | Skill Practice (e.g., coding) | Active Recall Session |
    | Wed | Catch-up/Review Day | Peer Study Session | Light Reading |
    | Thu | Math/Science Practice | Creative Project Work | Review Weakest Subject |
    | Fri | Test Preparation | Organizational Tasks | Leisure/Rest |
    | Sat | Deep Focus Block (3-4 hours) | Hands-on Experiment/Field Trip | Full Rest Day |
    | Sun | Planning & Preparation | Light Review Only | Mental Reset |

    ### 3. Resources to Use
    * **Digital Tools:** Quizlet or Anki for spaced repetition flashcards.
    * **Physical:** Use color-coded notes and highlighters for visual organization.
    * **Support:** Schedule weekly check-ins with a teacher or mentor.

    ### 4. Study Strategies for Difficult Topics
    * **Simplify:** Explain the concept aloud to an imaginary person (Feynman Technique).
    * **Visualize:** Draw diagrams, mind maps, or flowcharts instead of just reading text.
    * **Break Down:** Divide large, complex topics into 3-4 smaller, manageable sub-components.

    This plan is designed to be flexible. Remember to celebrate small victories!
    """

    return textwrap.dedent(plan_template).strip()


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

def add_student():
    name = input("Enter student name: ")
    needs = input("Enter special learning needs (e.g., visual learner, needs structure, or leave blank): ")
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
    print("\n--- Current Students ---")
    cursor.execute("SELECT id, name, special_needs FROM students")
    students = cursor.fetchall()
    if not students:
        print("No students currently enrolled.")
        return
    for s in students:
        print(f"ID: {s[0]} | Name: {s[1]} | Needs: {s[2] if s[2] else 'None'}")

def list_teachers():
    print("\n--- Current Teachers ---")
    cursor.execute("SELECT id, name, available_slots FROM teachers")
    teachers = cursor.fetchall()
    if not teachers:
        print("No teachers registered.")
        return
    for t in teachers:
        print(f"ID: {t[0]} | Name: {t[1]} | Slots: {t[2]}")

def is_slot_free(teacher_id, date, time):
    cursor.execute("SELECT * FROM classes WHERE teacher_id=? AND date=? AND time=?", (teacher_id, date, time))
    return cursor.fetchone() is None

def schedule_class():
    list_students()
    try:
        student_id = int(input("Enter student ID to schedule: "))
    except ValueError:
        print("Invalid student ID.")
        return

    list_teachers()
    try:
        teacher_id = int(input("Enter teacher ID: "))
    except ValueError:
        print("Invalid teacher ID.")
        return
        
    date = input("Enter date (YYYY-MM-DD): ")
    time = input("Enter time (HH:MM): ")
    subject = input("Enter subject: ")
    
    try:
        datetime.strptime(date, '%Y-%m-%d')
        datetime.strptime(time, '%H:%M')
    except ValueError:
        print("Invalid date or time format. Please use YYYY-MM-DD and HH:MM.")
        return

    if is_slot_free(teacher_id, date, time):
        cursor.execute(
            "INSERT INTO classes (student_id, teacher_id, date, time, subject) VALUES (?, ?, ?, ?, ?)",
            (student_id, teacher_id, date, time, subject)
        )
        conn.commit()
        print(f"\nClass scheduled successfully for Student {student_id}!")
    else:
        print("\nConflict detected: Teacher not available at this time.")

def generate_study_plan():
    list_students()
    try:
        student_id = int(input("Enter student ID to generate study plan: "))
    except ValueError:
        print("Invalid student ID.")
        return

    cursor.execute("SELECT name, special_needs FROM students WHERE id=?", (student_id,))
    student = cursor.fetchone()
    if student:
        name, needs = student
        plan = generate_ai_study_plan(name, needs)
        print("\n" + "="*50)
        print("    STUDY PLAN GENERATED (MOCK AI)")
        print("="*50)
        print(plan)
        print("="*50)
    else:
        print("Student not found.")

def main():
    while True:
        print("\n--- Student Scheduling & Mock Planner System ---")
        print("1. Add Student")
        print("2. Add Teacher")
        print("3. List Students")
        print("4. List Teachers")
        print("5. Schedule Class")
        print("6. Generate Study Plan (Mock AI)")
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
            print("Closing database connection and exiting...")
            conn.close()
            break
        else:
            print("Invalid choice! Try again.")

if __name__ == "__main__":
    main()