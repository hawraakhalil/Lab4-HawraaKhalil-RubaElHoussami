from src_ruba.components.instructor import Instructor
from src_ruba.components.student import Student
from src_ruba.components.course import Course

from src_ruba.utils.data_validator import DataValidator
from ..managers.data_manager import DataManager

import os

directory = os.getcwd()
manager = DataManager(directory)
validator = DataValidator()
students, instructors, courses = manager.boot()

student_id = len(students) + 1
instructor_id = len(instructors) + 1
course_id = len(courses) + 1


"""
STUDENT CONTROLLERS
"""

def register_student(name: str, age: int, email: str) -> tuple:
    global students, student_id
    if validator.validate_email(email) and validator.validate_age(age):
        student = Student(name, age, email, student_id)
        students[student_id] = student
        student_id += 1
        return {"message": f'Student with ID {student_id - 1} registered successfully', "student": student}, 200
    return {"message": "Invalid email or age"}, 400

def add_student_to_course(student_id: int, course_id: int) -> tuple:
    global students, courses
    if student_id in students and course_id in courses:
        student = students[student_id]
        course = courses[course_id]
        course.add_student(student)
        return {"message": "Student added to course successfully"}, 200
    return {"message": "Student or course not found"}, 404

def remove_student_from_course(student_id: int, course_id: int) -> tuple:
    global students, courses
    if student_id in students and course_id in courses:
        student = students[student_id]
        course = courses[course_id]
        if course.remove_student(student):
            return {"message": "Student removed from course successfully"}, 200
        return {"message": "Student is not registered in course"}, 400
    return {"message": "Student or course not found"}, 404

def remove_student(student_id: int) -> tuple:
    global students
    if student_id in students:
        student = students[student_id]
        for course_id in student.registered_courses:
            course = courses[course_id]
            course.remove_student(student)
        del students[student_id]
        return {"message": "Student deleted successfully"}, 200
    return {"message": "Student not found"}, 404

def get_students():
    global students
    return {"students": students}, 200

def get_students_by_course(course_id: int) -> dict:
    global courses
    if course_id in courses:
        course = courses[course_id]
        return {"students": course.students}, 200
    return {"message": "Course not found"}, 404

def get_student_courses(course_ids: list) -> dict:
    global courses
    courses_list = []
    for course_id in course_ids:
        if course_id in courses:
            courses_list.append(courses[course_id].name)
    return {"courses": courses_list}, 200

def get_student_id_by_name(student_name: str) -> dict:
    global students
    for student in students.values():
        if student.name == student_name:
            return {"student_id": student.student_id}, 200
    return {"message": "Student not found"}, 404

def search_students(search_type: str, search_term: str) -> dict:
    global students
    results = []
    if search_type == "name":
        for student_id in students:
            student = students[student_id]
            if student.name == search_term:
                results.append(student)
    elif search_type == "email":
        if validator.validate_email(search_term):
            for student_id in students:
                student = students[student_id]
                if student._email == search_term:
                    results.append(student)
        else:
            return {"message": "Invalid email"}, 400
    elif search_type == "id":
        if int(search_term) in students:
            results = [students[int(search_term)]]
    else:
        return {"message": "Invalid search type"}, 400
    return {"students": results}, 200


"""
INSTRUCTOR CONTROLLERS
"""


def register_instructor(name: str, age: int, email: str) -> Instructor:
    global instructors, instructor_id
    if validator.validate_email(email) and validator.validate_age(age):
        instructor = Instructor(name, age, email, instructor_id)
        instructors[instructor_id] = instructor
        instructor_id += 1
        return {"message": f'Instructor with ID {instructor_id - 1} registered successfully', "instructor": instructor}, 200
    return {"message": "Invalid email or age"}, 400

def add_instructor_to_course(instructor_id: int, course_id: int) -> tuple:
    global instructors, courses
    if instructor_id in instructors and course_id in courses:
        instructor = instructors[instructor_id]
        course = courses[course_id]
        course.add_instructor(instructor)
        return {"message": "Instructor added to course successfully"}, 200
    return {"message": "Instructor or course not found"}, 404

def remove_instructor_from_course(instructor_id: int, course_id: int) -> tuple:
    global instructors, courses
    if instructor_id in instructors and course_id in courses:
        instructor = instructors[instructor_id]
        course = courses[course_id]
        if course.remove_instructor(instructor):
            return {"message": "Instructor removed from course successfully"}, 200
        return {"message": "Instructor is not registered in course"}, 400
    return {"message": "Instructor or course not found"}, 404

def remove_instructor(instructor_id: int) -> tuple:
    global instructors
    if instructor_id in instructors:
        instructor = instructors[instructor_id]
        for course_id in instructor.assigned_courses:
            course = courses[course_id]
            course.remove_instructor(instructor)
        del instructors[instructor_id]
        return {"message": "Instructor deleted successfully"}, 200
    return {"message": "Instructor not found"}, 404

def get_instructors() -> dict:
    global instructors
    return {"instructors": instructors}, 200

def get_instructors_by_course(course_id: int) -> dict:
    global courses
    if course_id in courses:
        course = courses[course_id]
        return {"instructors": course.instructors}, 200
    return {"message": "Course not found"}, 404

def search_instructors(search_type: str, search_term: str) -> dict:
    global instructors
    results = []
    if search_type == "name":
        for instructor_id in instructors:
            instructor = instructors[instructor_id]
            if instructor.name == search_term:
                results.append(instructor)
    elif search_type == "email":
        if validator.validate_email(search_term):
            for instructor_id in instructors:
                instructor = instructors[instructor_id]
                if instructor._email == search_term:
                    results.append(instructor)
        else:
            return {"message": "Invalid email"}, 400
    elif search_type == "id":
        if int(search_term) in instructors:
            results = [instructors[int(search_term)]]
    else:
        return {"message": "Invalid search type"}, 400
    return {"instructors": results}, 200

def get_instructor_id_by_name(instructor_name: str) -> dict:
    global instructors
    for instructor in instructors.values():
        if instructor.name == instructor_name:
            return {"instructor_id": instructor.instructor_id}, 200
    return {"message": "Instructor not found"}, 404

def get_instructor_courses(course_ids: list) -> dict:
    global courses
    courses_list = []
    for course_id in course_ids:
        if course_id in courses:
            courses_list.append(courses[course_id].name)
    return {"courses": courses_list}, 200


"""
COURSE CONTROLLERS
"""


def add_course(name: str, description: str) -> Course:
    global courses, course_id
    course = Course(name, description,  course_id)
    courses[course_id] = course
    course_id += 1
    return {"message": f'Course with ID {course_id - 1} added successfully', "course": course}, 200

def remove_course(course_id: int) -> tuple:
    global courses
    if course_id in courses:
        course = courses[course_id]
        for student_id in course.students:
            student = course.students[student_id]
            student._unregister_course(course_id)
        for instructor_id in course.instructors:
            instructor = course.instructors[instructor_id]
            instructor._remove_course(course_id)
        del courses[course_id]
        return {"message": "Course deleted successfully"}, 200
    return {"message": "Course not found"}, 404

def get_courses() -> dict:
    global courses
    return {"courses": courses}, 200

def get_course_id_by_name(course_name: str) -> dict:
    global courses
    for course in courses.values():
        if course.name == course_name:
            return {"course_id": course.course_id}, 200
    return {"message": "Course not found"}, 404

def search_courses(search_type: str, search_term: str) -> dict:
    global courses
    results = []
    if search_type == "name":
        for course_id in courses:
            course = courses[course_id]
            if course.name.lower() == search_term.lower():
                results.append(course)
    elif search_type == "id":
        course_id = int(search_term)
        if course_id in courses:
            results = [courses[course_id]]
    else:
        return {"message": "Invalid search type"}, 400
    return {"courses": courses}, 200
    

def terminate() -> tuple:
    global students, instructors, courses
    return students, instructors, courses