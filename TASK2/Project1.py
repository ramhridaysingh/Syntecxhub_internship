                    #Project:1 -Student Management System                       

import json
import os


# ---------- Student Class ----------
class Student:
    def __init__(self, student_id, name, grade):
        self.id = student_id
        self.name = name
        self.grade = grade

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "grade": self.grade
        }


# ---------- Student Manager ----------
class StudentManager:
    FILE_NAME = "students.json"

    def __init__(self):
        self.students = self.load_students()

    def load_students(self):
        if os.path.exists(self.FILE_NAME):
            with open(self.FILE_NAME, "r") as file:
                return json.load(file)
        return []

    def save_students(self):
        with open(self.FILE_NAME, "w") as file:
            json.dump(self.students, file, indent=4)

    def is_unique_id(self, student_id):
        for student in self.students:
            if student["id"] == student_id:
                return False
        return True

    def add_student(self, student):
        if not self.is_unique_id(student.id):
            print(" Student ID already exists.")
            return
        self.students.append(student.to_dict())
        self.save_students()
        print("Student added successfully.")

    def update_student(self, student_id):
        for student in self.students:
            if student["id"] == student_id:
                student["name"] = input("Enter new name: ")
                student["grade"] = input("Enter new grade: ")
                self.save_students()
                print("Student updated successfully.")
                return
        print("Student not found.")

    def delete_student(self, student_id):
        for student in self.students:
            if student["id"] == student_id:
                self.students.remove(student)
                self.save_students()
                print("Student deleted successfully.")
                return
        print("Student not found.")

    def list_students(self):
        if not self.students:
            print("No student records found.")
            return

        print("\n--- Student Records ---")
        print(f"{'ID':<10}{'Name':<20}{'Grade'}")
        print("-" * 40)
        for student in self.students:
            print(f"{student['id']:<10}{student['name']:<20}{student['grade']}")
        print("-" * 40)

def main():
    manager = StudentManager()

    while True:
        print("\n--- Student Management System ---")
        print("1. Add Student")
        print("2. Update Student")
        print("3. Delete Student")
        print("4. List Students")
        print("5. Exit")

        choice = input("Choose an option (1-5): ")

        if choice == "1":
            sid = input("Enter Student ID: ")
            name = input("Enter Student Name: ")
            grade = input("Enter Grade: ")
            student = Student(sid, name, grade)
            manager.add_student(student)

        elif choice == "2":
            sid = input("Enter Student ID to update: ")
            manager.update_student(sid)

        elif choice == "3":
            sid = input("Enter Student ID to delete: ")
            manager.delete_student(sid)

        elif choice == "4":
            manager.list_students()

        elif choice == "5":
            print("Exiting program. Goodbye 👋")
            break

        else:
            print("Invalid choice. Try again.")


# ----- Run Program -----
main()
