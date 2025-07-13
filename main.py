# Student Grade Management System (Admin Protected + PDF Report)
# Run using: python main.py

from fpdf import FPDF

students = {}

# Admin credentials
ADMIN_NAME = "admin"
ADMIN_PASSWORD = "pass123"

def login():
    print("\n🔐 Admin Login Required")
    attempts = 3
    while attempts > 0:
        name = input("Enter admin name: ").strip()
        password = input("Enter password: ").strip()

        if name == ADMIN_NAME and password == ADMIN_PASSWORD:
            print("\n✅ Login successful! Access granted.\n")
            return True
        else:
            attempts -= 1
            print(f"❌ Invalid credentials. Attempts left: {attempts}")
    
    print("🚫 Too many failed attempts. Exiting system.")
    return False

def welcome():
    print("\n--- Welcome to the Student Grade Management System ---")
    print("-" * 60)

def menu():
    print("\nPlease choose an option:")
    print("1. Add Student and Grade")
    print("2. View All Students and Their Grades")
    print("3. View Class Average Grade")
    print("4. Generate PDF Report")
    print("5. Exit")

def add_student():
    name = input("\nEnter student name: ").strip().title()
    if not name:
        print("⚠ Name cannot be empty.")
        return

    branch = input("Enter branch (e.g., CSE, ECE): ").strip().upper()
    section = input("Enter section (e.g., A, B): ").strip().upper()
    subject = input("Enter subject name: ").strip().title()

    try:
        grade = float(input("Enter grade (0-100): "))
        if 0 <= grade <= 100:
            student_record = {
                "branch": branch,
                "section": section,
                "subject": subject,
                "grade": grade
            }
            if name in students:
                students[name].append(student_record)
            else:
                students[name] = [student_record]
            print(f"✅ Successfully added {subject} grade {grade} for {name}.")
        else:
            print("⚠ Grade must be between 0 and 100.")
    except ValueError:
        print("⚠ Invalid input! Please enter a number.")

def view_students():
    if not students:
        print("\nNo students added yet.")
        return

    print("\nStudent Details and Grades:")
    print("-" * 60)
    for name, records in students.items():
        print(f"\n{name}:")
        for record in records:
            print(f"   Subject: {record['subject']} | Branch: {record['branch']} | Section: {record['section']} | Grade: {record['grade']}")
    print("-" * 60)

def class_average():
    if not students:
        print("\nNo grades available to calculate class average.")
        return

    total = 0
    count = 0
    for records in students.values():
        for record in records:
            total += record['grade']
            count += 1
    class_avg = total / count
    print(f"\nClass Average Grade: {class_avg:.2f}")

def generate_pdf_report():
    if not students:
        print("\n⚠ No data to generate report.")
        return

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Student Grade Report", ln=True, align="C")
    pdf.ln(5)

    pdf.set_font("Arial", "", 12)

    for name, records in students.items():
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, f"Student: {name}", ln=True)
        pdf.set_font("Arial", "", 12)
        for record in records:
            line = f"   Subject: {record['subject']}, Branch: {record['branch']}, Section: {record['section']}, Grade: {record['grade']}"
            pdf.cell(0, 8, line, ln=True)
        pdf.ln(4)

    total = sum(record['grade'] for records in students.values() for record in records)
    count = sum(len(records) for records in students.values())
    class_avg = total / count if count else 0

    pdf.set_font("Arial", "B", 12)
    pdf.ln(5)
    pdf.cell(0, 10, f"Class Average Grade: {class_avg:.2f}", ln=True)

    pdf.output("student_report.pdf")
    print("\n✅ PDF report generated: student_report.pdf")

def start():
    if not login():
        return

    welcome()
    while True:
        menu()
        choice = input("Enter your choice (1-5): ").strip()

        if choice == '1':
            add_student()
        elif choice == '2':
            view_students()
        elif choice == '3':
            class_average()
        elif choice == '4':
            generate_pdf_report()
        elif choice == '5':
            print("\n👋 Thank you for using the Student Grade Manager. Goodbye!\n")
            break
        else:
            print("⚠ Invalid choice. Please enter a number between 1 and 5.")

# Run the program
if __name__ == "__main__":
    start()

