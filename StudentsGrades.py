import database

# Helper functions
def input_grade_component(component_name):
    """Helper function to input grades for a specific component."""
    while True:
        try:
            grade = float(input(f"Enter {component_name} grade (0-100): "))
            if 0 <= grade <= 100:
                return grade
            else:
                print("Grade must be between 0 and 100.")
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

def compute_final_grade(written_works, performance_tasks, quarterly_assessment):
    """Compute the final grade based on DepEd grading weights."""
    written_weight = 0.30
    performance_weight = 0.50
    quarterly_weight = 0.20

    final_grade = (
        (written_works * written_weight) +
        (performance_tasks * performance_weight) +
        (quarterly_assessment * quarterly_weight)
    )
    return round(final_grade, 2)

# Core functionalities
def input_grades_for_student(student):
    """Input grades for a single student."""
    print(f"\nEntering grades for {student['name']} (Grade {student['grade_level']}):")

    grades = {}
    for subject in ["English", "Science", "Math"]:
        print(f"\n{subject}:")
        written = input_grade_component("Written Works")
        performance = input_grade_component("Performance Tasks")
        quarterly = input_grade_component("Quarterly Assessment")

        final_grade = compute_final_grade(written, performance, quarterly)
        grades[subject] = {
            "Written Works": written,
            "Performance Tasks": performance,
            "Quarterly Assessment": quarterly,
            "Final Grade": final_grade
        }

    student["grades"] = grades
    print(f"\nGrades successfully updated for {student['name']}!")

def input_student_grades():
    """Input grades for students."""
    all_students = database.fetch_all("students")

    if not all_students:
        print("No students found. Please add students first.")
        return

    print("\n=== Input Grades ===")
    print("1. Input grades for a single student")
    print("2. Input grades for all students")

    choice = input("Select an option: ").strip()

    if choice == '1':
        for idx, student in enumerate(all_students, 1):
            print(f"{idx}. {student['name']} (Grade {student['grade_level']})")

        try:
            student_id = int(input("Enter the student ID to input grades: ")) - 1
            if not (0 <= student_id < len(all_students)):
                print("Invalid student ID.")
                return
        except ValueError:
            print("Invalid input. Please enter a numeric value.")
            return

        student = all_students[student_id]
        input_grades_for_student(student)

    elif choice == '2':
        for student in all_students:
            input_grades_for_student(student)

    else:
        print("Invalid choice. Returning to menu.")
        return

    # Save updated grades to the database
    database.save_all("students", all_students)

def generate_reports():
    """Generate student grade reports including averages and rankings."""
    all_students = database.fetch_all("students")

    if not all_students:
        print("No students found. Please add students first.")
        return

    print("\n=== Generating Reports ===")
    rankings = []

    for student in all_students:
        grades = student.get('grades', {})
        total_grades = 0
        num_subjects = len(grades)

        print(f"\nReport for {student['name']} (Grade {student['grade_level']}):")
        print("Subject Grades:")

        for subject, details in grades.items():
            final_grade = details.get("Final Grade", 0)
            total_grades += final_grade
            print(f"  {subject}: {final_grade}%")

        average = round(total_grades / num_subjects, 2) if num_subjects > 0 else 0
        print(f"Average Grade: {average}%")

        if average >= 98:
            rank = "With Highest Honor"
        elif 95 <= average < 98:
            rank = "With High Honor"
        elif 90 <= average < 95:
            rank = "With Honor"
        elif average >= 75:
            rank = "Passed"
        else:
            rank = "Failed"

        print(f"Rank: {rank}")

        rankings.append({
            "name": student['name'],
            "average": average,
            "rank": rank
        })

    print("\n=== Rankings ===")
    rankings.sort(key=lambda x: x['average'], reverse=True)
    for idx, entry in enumerate(rankings, 1):
        print(f"{idx}. {entry['name']} - Average: {entry['average']}% - {entry['rank']}")

def grading_menu():
    """Menu for grading system."""
    while True:
        print("================================================================")
        print("                 === Grading System ===")
        print("----------------------------------------------------------------")
        print("1. Input Grades for Students")
        print("2. Generate Student Reports and Rankings")
        print("3. Go Back")
        print("================================================================")

        choice = input("Select an option: ").strip()
        if choice == '1':
            input_student_grades()
        elif choice == '2':
            generate_reports()
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")
