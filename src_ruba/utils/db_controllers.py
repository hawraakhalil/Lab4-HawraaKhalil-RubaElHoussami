import sqlite3
import os
from src.utils.data_validator import DataValidator
from src.components.student import Student
from src.components.instructor import Instructor
from src.components.course import Course

validator = DataValidator()

def initialize_database():
    db_file = 'school_management_system.db'
    db_exists = os.path.exists(db_file)
    
    conn = get_db_connection()

    if not db_exists:
        create_tables(conn)
        return {"message": "Database created and initialized successfully"}, 200
    else:
        return {"message": "Database already exists"}, 200

def get_db_connection():
    conn = sqlite3.connect('school_management_system.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_tables(conn):
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        email TEXT UNIQUE NOT NULL
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS instructors (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        email TEXT UNIQUE NOT NULL
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        description TEXT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS registrations (
        student_id INTEGER,
        course_id INTEGER,
        FOREIGN KEY (student_id) REFERENCES students (id),
        FOREIGN KEY (course_id) REFERENCES courses (id),
        PRIMARY KEY (student_id, course_id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS course_instructors (
        instructor_id INTEGER,
        course_id INTEGER,
        FOREIGN KEY (instructor_id) REFERENCES instructors (id),
        FOREIGN KEY (course_id) REFERENCES courses (id),
        PRIMARY KEY (instructor_id, course_id)
    )
    ''')
    
    conn.commit()

def backup_database(backup_file: str):
    try:
        backup_conn = sqlite3.connect(backup_file)
        
        with sqlite3.connect('school_management.db') as conn:
            conn.backup(backup_conn)
        backup_conn.close()
        return {"message": "Database backup created successfully"}, 200
    except sqlite3.Error as e:
        return {"message": f"An error occurred: {e}"}, 500
    

"""
STUDENT CONTROLLERS
"""

def register_student(name: str, age: int, email: str) -> tuple:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        if validator.validate_email(email) and validator.validate_age(age):
            cursor.execute('INSERT INTO students (name, age, email) VALUES (?, ?, ?)', (name, age, email))
            conn.commit()
            return {"message": f'Student registered successfully', "student_id": cursor.lastrowid}, 200
        return {"message": "Invalid email or age"}, 400
    except sqlite3.IntegrityError:
        return {"message": "Email already exists"}, 400
    finally:
        conn.close()

def add_student_to_course(student_id: int, course_id: int) -> tuple:
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO registrations (student_id, course_id) VALUES (?, ?)', (student_id, course_id))
        conn.commit()
        return {"message": "Student added to course successfully"}, 200
    except sqlite3.IntegrityError:
        return {"message": "Student or course not found"}, 404
    
def remove_student_from_course(student_id: int, course_id: int) -> tuple:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM registrations WHERE student_id = ? AND course_id = ?', (student_id, course_id))
    conn.commit()
    if cursor.rowcount == 0:
        conn.close()
        return {"message": "Student not registered in course or course/student not found"}, 404
    conn.close()
    return {"message": "Student removed from course successfully"}, 200

def remove_student(student_id: int) -> tuple:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM students WHERE id = ?', (student_id,))
    conn.commit()
    if cursor.rowcount == 0:
        conn.close()
        return {"message": "Student not found"}, 404
    conn.close()
    return {"message": "Student deleted successfully"}, 200

def get_students():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students')
    students_data = cursor.fetchall()
    conn.close()
    students = {}
    for student in students_data:
        students[student['id']] = Student(student['name'], student['age'], student['email'], student['id'])
    return {"students": students}, 200

def get_students_by_course(course_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students WHERE course_id = ?', (course_id,))
    students_data = cursor.fetchall()
    conn.close()
    students = {}
    for student in students_data:
        students[student['id']] = Student(student['name'], student['age'], student['email'], student['id'])
    return {"students": students}, 200

def get_student_courses(student_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT c.* FROM courses c
        JOIN registrations r ON c.id = r.course_id
        WHERE r.student_id = ?
    ''', (student_id,))
    courses_data = cursor.fetchall()
    conn.close()
    courses = {}
    for course in courses_data:
        courses[course['id']] = Course(course['name'], course['age'], course['email'], course['id'])
    return {"students": courses}, 200

def get_student_id_by_name(student_name: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students WHERE name = ?', (student_name,))
    student = cursor.fetchone()
    conn.close()
    return {"student_id": student['id']}, 200

def search_students(search_type: str, search_term: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    if search_type == "name":
        cursor.execute('SELECT * FROM students WHERE name LIKE ?', (f'%{search_term}%',))
    elif search_type == "email":
        cursor.execute('SELECT * FROM students WHERE email = ?', (search_term,))
    elif search_type == "id":
        cursor.execute('SELECT * FROM students WHERE id = ?', (search_term,))
    else:
        conn.close()
        return {"message": "Invalid search type"}, 400
    students_data = cursor.fetchall()
    conn.close()
    courses = {}
    for course in courses_data:
        courses[course['id']] = Student(course['name'], course['age'], course['email'], course['id'])
    return {"students": courses}, 200

def update_student(student_id: int, name: str, age: int, email: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('UPDATE students SET name = ?, age = ?, email = ? WHERE id = ?', (name, age, email, student_id))
        conn.commit()
        if cursor.rowcount == 0:
            return {"message": "Student not found"}, 404
        return {"message": "Student updated successfully"}, 200
    except sqlite3.IntegrityError:
        return {"message": "Email already exists"}, 400
    finally:
        conn.close()


"""
INSTRUCTOR CONTROLLERS
"""


def register_instructor(name: str, age: int, email: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO instructors (name, age, email) VALUES (?, ?, ?)', (name, age, email))
        conn.commit()
        return {"message": f'Instructor registered successfully', "instructor_id": cursor.lastrowid}, 200
    except sqlite3.IntegrityError:
        return {"message": "Email already exists"}, 400
    finally:
        conn.close()

def add_instructor_to_course(instructor_id: int, course_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO course_instructors (instructor_id, course_id) VALUES (?, ?)', (instructor_id, course_id))
        conn.commit()
        return {"message": "Instructor added to course successfully"}, 200
    except sqlite3.IntegrityError:
        return {"message": "Instructor or course not found, or instructor already assigned"}, 400
    finally:
        conn.close()

def remove_instructor_from_course(instructor_id: int, course_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM course_instructors WHERE instructor_id = ? AND course_id = ?', (instructor_id, course_id))
    if cursor.rowcount == 0:
        conn.close()
        return {"message": "Instructor not assigned to course or course/instructor not found"}, 404
    conn.close()
    return {"message": "Instructor removed from course successfully"}, 200

def remove_instructor(instructor_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM instructors WHERE id = ?', (instructor_id,))
    conn.commit()
    if cursor.rowcount == 0:
        conn.close()
        return {"message": "Instructor not found"}, 404
    conn.close()
    return {"message": "Instructor deleted successfully"}, 200

def get_instructors():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM instructors')
    instructors_data = cursor.fetchall()
    conn.close()
    instructors = [Instructor(instructor['name'], instructor['age'], instructor['email'], instructor['id']) for instructor in instructors_data]
    return {"instructors": instructors}, 200

def get_students_by_course(course_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT s.* FROM students s
        JOIN registrations r ON s.id = r.student_id
        WHERE r.course_id = ?
    ''', (course_id,))
    students_data = cursor.fetchall()
    conn.close()
    students = [Student(student['name'], student['age'], student['email'], student['id']) for student in students_data]
    return {"students": students}, 200

def get_instructors_by_course(course_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT i.* FROM instructors i
        JOIN course_instructors ci ON i.id = ci.instructor_id
        WHERE ci.course_id = ?
    ''', (course_id,))
    instructors_data = cursor.fetchall()
    conn.close()
    instructors = [Instructor(instructor['name'], instructor['age'], instructor['email'], instructor['id']) for instructor in instructors_data]
    return {"instructors": instructors}, 200

def search_instructors(search_type: str, search_term: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    if search_type == "name":
        cursor.execute('SELECT * FROM instructors WHERE name LIKE ?', (f'%{search_term}%',))
    elif search_type == "email":
        cursor.execute('SELECT * FROM instructors WHERE email = ?', (search_term,))
    elif search_type == "id":
        cursor.execute('SELECT * FROM instructors WHERE id = ?', (search_term,))
    else:
        conn.close()
        return {"message": "Invalid search type"}, 400
    instructors_data = cursor.fetchall()
    conn.close()
    instructors = [Instructor(instructor['name'], instructor['age'], instructor['email'], instructor['id']) for instructor in instructors_data]
    return {"instructors": instructors}, 200

def get_instructor_id_by_name(instructor_name: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM instructors WHERE name = ?', (instructor_name,))
    instructor = cursor.fetchone()
    if instructor is None:
        conn.close()
        return {"message": "Instructor not found"}, 404
    conn.close()
    return {"instructor_id": instructor[0]}, 200

def get_instructor_courses(instructor_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM courses WHERE instructor_id = ?', (instructor_id,))
    courses = cursor.fetchall()
    conn.close()
    courses = [Course(course['name'], course['description'], course['id']) for course in courses]
    return {"courses": courses}, 200

def update_instructor(instructor_id: int, name: str, age: int, email: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('UPDATE instructors SET name = ?, age = ?, email = ? WHERE id = ?', (name, age, email, instructor_id))
        conn.commit()
        if cursor.rowcount == 0:
            return {"message": "Instructor not found"}, 404
        return {"message": "Instructor updated successfully"}, 200
    except sqlite3.IntegrityError:
        return {"message": "Email already exists"}, 400
    finally:
        conn.close()


"""
COURSE CONTROLLERS
"""


def add_course(name: str, description: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO courses (name, description) VALUES (?, ?)', (name, description))
    conn.commit()
    course_id = cursor.lastrowid
    conn.close()
    return {"message": f'Course added successfully', "course_id": course_id}, 200

def remove_course(course_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM courses WHERE id = ?', (course_id,))
    conn.commit()
    if cursor.rowcount == 0:
        conn.close()
        return {"message": "Course not found"}, 404
    conn.close()
    return {"message": "Course deleted successfully"}, 200

def get_courses():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM courses')
    courses = cursor.fetchall()
    conn.close()
    courses = [Course(course['name'], course['description'], course['id']) for course in courses]
    return {"courses": courses}, 200

def get_course_id_by_name(course_name: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM courses WHERE name = ?', (course_name,))
    course = cursor.fetchone()
    if course is None:
        conn.close()
        return {"message": "Course not found"}, 404
    conn.close()
    return {"course_id": course[0]}, 200

def search_courses(search_type: str, search_term: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    if search_type == "name":
        cursor.execute('SELECT * FROM courses WHERE name LIKE ?', (f'%{search_term}%',))
    elif search_type == "id":
        cursor.execute('SELECT * FROM courses WHERE id = ?', (search_term,))
    else:
        conn.close()
        return {"message": "Invalid search type"}, 400
    courses = cursor.fetchall()
    conn.close()
    courses = [Course(course['name'], course['description'], course['id']) for course in courses]
    return {"courses": courses}, 200

def update_course(course_id: int, name: str, description: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE courses SET name = ?, description = ? WHERE id = ?', (name, description, course_id))
    conn.commit()
    if cursor.rowcount == 0:
        conn.close()
        return {"message": "Course not found"}, 404
    conn.close()
    return {"message": "Course updated successfully"}, 200
