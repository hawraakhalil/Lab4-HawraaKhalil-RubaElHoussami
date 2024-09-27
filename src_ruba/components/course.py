from .student import Student
from .instructor import Instructor

class Course:
    def __init__(self, name: str, description:str, course_id: str):
        self.name = name
        self.description = description
        self.course_id = course_id
        self.students = {}
        self.instructors = {}
    
    def add_student(self, student: Student):
        self.students[student.student_id] = student
        student._register_course(self.course_id)
    
    def remove_student(self, student: Student):
        if student.student_id in self.students:
            del self.students[student.student_id]
            student._unregister_course(self.course_id)
            return True
        return False
    
    def add_instructor(self, instructor: Instructor):
        self.instructors[instructor.instructor_id] = instructor
        instructor._add_course(self.course_id)
    
    def remove_instructor(self, instructor: Instructor):
        if instructor.instructor_id in self.instructors:
            del self.instructors[instructor.instructor_id]
            instructor._remove_course(self.course_id)
            return True
        return False

    def __repr__(self):
        """
        This method returns a string representation of the object which will be needed for pickling.
        """
        return f"Course(name={self.name}, description={self.description}, course_id={self.course_id}, students={self.students}, instructors={self.instructors})"