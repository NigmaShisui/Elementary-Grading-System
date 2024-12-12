import database

#print students list
def view_students():
    students = database.fetch_all('students')
    if not students:
        print('No students found.')
        return

    print("\nList of Students:")
    for idx, student in enumerate(students, 1):
        print(f"{idx}. {student['name']} - {student['grade_level']}")

#add or append student to the dataabase
def add_student():
    name = input("Enter student name: ").strip()
    grade_level = input("Enter grade level (e.g., Grade 1 to Grade 6.): ").strip()

    # Capitalize the first letter of each word
    formatted_name = name.title()
    formatted_grade_level = grade_level.title()

    # Validate grade level
    if formatted_grade_level.startswith("Grade"):
        try:
            grade_number = int(formatted_grade_level.split()[1])
            if grade_number < 1 or grade_number > 6:
                print("This is for elementary grade use only.")
                return
        except ValueError:
            print("Invalid grade level format. Please use 'Grade 1', 'to' 'Grade 6.")
            return
    else:
        print("Invalid grade level format. Please use 'Grade 1', 'to' 'Grade 6'.")
        return

    student = {
        "name": formatted_name,  # Save the formatted name
        "grade_level": formatted_grade_level,  # Save the formatted grade level
        "grades": {}
    }
    students = database.fetch_all('students')
    students.append(student)
    database.save_all('students', students)
    print(f"Student {formatted_name} added successfully!")


#remove student from database
def remove_student():
    students = database.fetch_all('students')
    if not students:
        print("No students to remove.")
        return
    
    view_students()
    student_id = int(input("Enter student ID to remove: ")) - 1
    if 0 <= student_id < len(students):
        removed_student = students.pop(student_id)
        database.save_all('students', students)
        print(f"Student {removed_student['name']} removed successfully!")
    else:
        print("Invalid student ID.")

#clear all students from the database
def clear_students():
    confirm = input("Are you sure you want to clear all students? (y/n): ")
    if confirm.lower() == 'y':
        database.save_all('students', [])
        print("All students cleared.")
    else:
        print("Operation cancelled.")

#sort students
def sort_students():
    students = database.fetch_all('students')
    if not students:
        print("No students found to sort.")
        return
    
    print("\n=== Sort Students ===")
    print("1. Sort by Grade Level")
    print("2. Sort by Name")
    choice = input("Select a sorting option: ").strip()

    if choice == '1':
        students.sort(key=lambda x: (int(x['grade_level'].split()[1]) if 'Grade' in x['grade_level'] else 999, x['grade_level']))
        print("Students sorted by Grade Level.")
    elif choice == '2':
        students.sort(key=lambda x: x['name'].lower())
        print("Students sorted by Name.")
    else:
        print("Invalid choice.")
        return

    database.save_all('students', students)
    view_students()

#update students name or any
def update_student():
    students = database.fetch_all('students')
    if not students:
        print("No students to update.")
        return

    view_students()
    try:
        student_id = int(input("Enter student ID to update: ")) - 1
    except ValueError:
        print("Invalid input. Please enter a numeric ID.")
        return

    if 0 <= student_id < len(students):
        student = students[student_id]
        print(f"Updating student {student['name']}")

        # Accept user input and capitalize the first letter of each word
        name = input(f"Enter new name (current: {student['name']}): ").strip()
        formatted_name = name.title()  # Capitalize first letters

        grade_level = input(f"Enter new grade level (current: {student['grade_level']}): ").strip()
        formatted_grade_level = grade_level.title()  # Capitalize first letters

        # Validate grade level
        if formatted_grade_level.startswith("Grade"):
            try:
                grade_number = int(formatted_grade_level.split()[1])
                if grade_number < 1 or grade_number > 6:
                    print("This is for elementary grade use only.")
                    return
            except ValueError:
                print("Invalid grade level format. Please use 'Grade 1', 'Grade 2', etc.")
                return
        else:
            print("Invalid grade level format. Please use 'Grade 1', 'Grade 2', etc.")
            return

        # Update the student's information in the database
        student['name'] = formatted_name
        student['grade_level'] = formatted_grade_level
        database.save_all('students', students)
        print(f"Student {formatted_name} updated successfully!")
    else:
        print("Invalid student ID.")


def manage_students_menu():
    while True:
        print("=================================")
        print("     === Manage Students ===")
        print("---------------------------------")
        print(" ")
        print("1. View Students")
        print("2. Add Student")
        print("3. Remove Student")
        print("4. Clear All Students")
        print("5. Sort Students")
        print("6. Update Student")
        print("7. Go Back")
        print(" ")
        print("=================================")

        choice = input("Select an option: ").strip()
        if choice == '1':
            view_students()
        elif choice == '2':
            add_student()
        elif choice == '3':
            remove_student()
        elif choice == '4':
            clear_students()
        elif choice == '5':
            sort_students()
        elif choice == '6':
            update_student()
        elif choice == '7':
            break
        else:
            print("Invalid choice. Please try again.")